"""Harness de verificação automatizada do ecossistema SOA (Marketplace com Pagamento)."""

import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid

IN_DOCKER = os.getenv("SOA_ENV") == "docker"
SERVICES = {
    "orquestrador": "http://orquestrador:8000" if IN_DOCKER else "http://localhost:8006",
    "catalogo": "http://catalogo:8001" if IN_DOCKER else "http://localhost:8001",
    "pedidos": "http://pedidos:8002" if IN_DOCKER else "http://localhost:8002",
    "pagamentos": "http://pagamentos:8003" if IN_DOCKER else "http://localhost:8003",
    "notificacoes": "http://notificacoes:8004" if IN_DOCKER else "http://localhost:8004",
}


def http_json(method: str, url: str, payload: dict | None = None, cid: str | None = None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"}
    if cid:
        headers["X-Correlation-ID"] = cid
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        return err.code, json.loads(err.read().decode("utf-8"))


def aguardar_healthchecks(timeout_s: int = 45):
    print("[HARNESS] 1. Verificando healthchecks dos 5 serviços SOA...")
    inicio = time.time()
    pendentes = dict(SERVICES)
    while pendentes and (time.time() - inicio) < timeout_s:
        for nome, base_url in list(pendentes.items()):
            url = f"{base_url}/health"
            try:
                status, body = http_json("GET", url)
                if status == 200 and body.get("status") == "ok":
                    print(f"  [OK] {nome} saudável ({url})")
                    pendentes.pop(nome)
            except Exception:
                pass
        if pendentes:
            time.sleep(1)
    if pendentes:
        raise RuntimeError(f"Serviços indisponíveis após {timeout_s}s: {list(pendentes.keys())}")


def main():
    aguardar_healthchecks()

    # Consultar estoque inicial
    status, prod_inicial = http_json("GET", f"{SERVICES['catalogo']}/produtos/prod-1")
    assert status == 200, f"Esperado 200, recebido {status}"
    estoque_inicial = prod_inicial["estoque"]
    print(f"\n[HARNESS] Estoque inicial prod-1: {estoque_inicial}")

    # Cenário 1: Fluxo Principal (Compra Aprovada + Split)
    cid1 = f"harness-ok-{uuid.uuid4().hex[:6]}"
    idem_key = f"idem-{uuid.uuid4().hex[:8]}"
    print(f"\n[HARNESS] 2. Executando Cenário 1: Compra Aprovada (cid={cid1}, key={idem_key})")
    status, resp1 = http_json(
        "POST",
        f"{SERVICES['orquestrador']}/checkout",
        {
            "comprador": "augusto@marketplace.local",
            "produto_id": "prod-1",
            "quantidade": 2,
            "metodo": "PIX",
            "idempotency_key": idem_key,
        },
        cid=cid1,
    )
    assert status == 200, f"Esperado 200, recebido {status}: {resp1}"
    assert resp1["status"] == "PAGO"
    assert resp1["pagamento"]["split"]["marketplace_comissao_10pct"] == 50.0
    assert resp1["pagamento"]["split"]["vendedor_repasse_90pct"] == 450.0
    print(f"  [OK] Pedido {resp1['pedido_id']} PAGO | Split: {resp1['pagamento']['split']}")

    _, prod_apos_compra = http_json("GET", f"{SERVICES['catalogo']}/produtos/prod-1")
    assert prod_apos_compra["estoque"] == estoque_inicial - 2
    print(f"  [OK] Estoque atualizado: {prod_apos_compra['estoque']}")

    # Cenário 2: Idempotência (mesma idempotency_key não cobra nem reduz estoque de novo)
    cid2 = f"harness-idem-{uuid.uuid4().hex[:6]}"
    print(f"\n[HARNESS] 3. Executando Cenário 2: Teste de Idempotência (cid={cid2}, key={idem_key})")
    status, resp2 = http_json(
        "POST",
        f"{SERVICES['orquestrador']}/checkout",
        {
            "comprador": "augusto@marketplace.local",
            "produto_id": "prod-1",
            "quantidade": 2,
            "metodo": "PIX",
            "idempotency_key": idem_key,
        },
        cid=cid2,
    )
    assert status == 200, f"Esperado 200, recebido {status}: {resp2}"
    assert resp2["pagamento"]["idempotente"] is True
    assert resp2["pagamento"]["transacao_id"] == resp1["pagamento"]["transacao_id"]
    _, prod_apos_idem = http_json("GET", f"{SERVICES['catalogo']}/produtos/prod-1")
    assert prod_apos_idem["estoque"] == estoque_inicial - 2
    print(f"  [OK] Idempotência confirmada (tx={resp2['pagamento']['transacao_id']}, estoque mantido={prod_apos_idem['estoque']})")

    # Cenário 3: Falha no Pagamento + Compensação SOA (Saga)
    cid3 = f"harness-fail-{uuid.uuid4().hex[:6]}"
    print(f"\n[HARNESS] 4. Executando Cenário 3: Pagamento Recusado + Compensação (cid={cid3})")
    status, resp3 = http_json(
        "POST",
        f"{SERVICES['orquestrador']}/checkout",
        {
            "comprador": "augusto@marketplace.local",
            "produto_id": "prod-1",
            "quantidade": 1,
            "metodo": "CARTAO",
            "idempotency_key": f"idem-fail-{uuid.uuid4().hex[:6]}",
            "simular_falha": True,
        },
        cid=cid3,
    )
    assert status == 402, f"Esperado 402, recebido {status}: {resp3}"
    assert resp3["status"] == "CANCELADO"
    assert resp3["compensacao_executada"] is True
    _, prod_apos_comp = http_json("GET", f"{SERVICES['catalogo']}/produtos/prod-1")
    assert prod_apos_comp["estoque"] == estoque_inicial - 2
    print(f"  [OK] Compensação executada: pedido {resp3['pedido_id']} CANCELADO, estoque restaurado={prod_apos_comp['estoque']}")

    # Verificar notificações registradas
    _, notifs = http_json("GET", f"{SERVICES['notificacoes']}/notificacoes")
    assert notifs["total"] >= 2
    print(f"\n[HARNESS] 5. Notificações registradas: {notifs['total']} eventos")
    print("[HARNESS] TODOS OS TESTES PASSARAM COM SUCESSO!")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[HARNESS] FALHA: {exc}", file=sys.stderr)
        sys.exit(1)
