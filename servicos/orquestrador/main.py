import logging
import os
import uuid
from typing import Literal
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | orquestrador | %(levelname)s | %(message)s",
)
logger = logging.getLogger("orquestrador")

app = FastAPI(title="Orquestrador SOA — Marketplace com Pagamento", version="1.0.0")

CATALOGO_URL = os.getenv("CATALOGO_URL", "http://catalogo:8001")
PEDIDOS_URL = os.getenv("PEDIDOS_URL", "http://pedidos:8002")
PAGAMENTOS_URL = os.getenv("PAGAMENTOS_URL", "http://pagamentos:8003")
NOTIFICACOES_URL = os.getenv("NOTIFICACOES_URL", "http://notificacoes:8004")


class CheckoutRequest(BaseModel):
    comprador: str
    produto_id: str
    quantidade: int = Field(gt=0)
    metodo: Literal["PIX", "CARTAO"]
    idempotency_key: str
    simular_falha: bool = False


@app.get("/health")
def health():
    return {"status": "ok", "servico": "orquestrador"}


@app.post("/checkout")
async def executar_checkout(body: CheckoutRequest, request: Request):
    cid = request.headers.get("X-Correlation-ID") or f"cid-{uuid.uuid4().hex[:8]}"
    headers = {"X-Correlation-ID": cid}

    logger.info(
        f"cid={cid} | Iniciando checkout SOA | comprador={body.comprador} "
        f"produto={body.produto_id} qtd={body.quantidade} metodo={body.metodo}"
    )

    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. Reservar estoque no Catálogo
        res_cat = await client.post(
            f"{CATALOGO_URL}/produtos/{body.produto_id}/reservar",
            json={"quantidade": body.quantidade},
            headers=headers,
        )
        if res_cat.status_code != 200:
            logger.warning(f"cid={cid} | Falha ao reservar estoque: {res_cat.text}")
            raise HTTPException(
                status_code=res_cat.status_code,
                detail=res_cat.json().get("detail", "Erro no catálogo"),
            )
        dados_prod = res_cat.json()
        valor_total = round(dados_prod["preco_unitario"] * body.quantidade, 2)

        # 2. Criar pedido PENDENTE no serviço de Pedidos
        res_ped = await client.post(
            f"{PEDIDOS_URL}/pedidos",
            json={
                "comprador": body.comprador,
                "produto_id": body.produto_id,
                "quantidade": body.quantidade,
                "valor_total": valor_total,
                "vendedor_id": dados_prod["vendedor_id"],
            },
            headers=headers,
        )
        res_ped.raise_for_status()
        pedido = res_ped.json()
        pedido_id = pedido["pedido_id"]

        # 3. Processar pagamento + split + idempotência
        res_pag = await client.post(
            f"{PAGAMENTOS_URL}/pagamentos",
            json={
                "pedido_id": pedido_id,
                "vendedor_id": dados_prod["vendedor_id"],
                "valor": valor_total,
                "metodo": body.metodo,
                "idempotency_key": body.idempotency_key,
                "simular_falha": body.simular_falha,
            },
            headers=headers,
        )

        if res_pag.status_code != 200:
            # Compensação SOA (Saga): libera estoque, cancela pedido e notifica
            logger.warning(
                f"cid={cid} | Pagamento recusado para {pedido_id}. Executando compensação SOA..."
            )
            await client.post(
                f"{CATALOGO_URL}/produtos/{body.produto_id}/liberar",
                json={"quantidade": body.quantidade},
                headers=headers,
            )
            await client.patch(
                f"{PEDIDOS_URL}/pedidos/{pedido_id}/status",
                json={"status": "CANCELADO"},
                headers=headers,
            )
            await client.post(
                f"{NOTIFICACOES_URL}/notificacoes",
                json={
                    "pedido_id": pedido_id,
                    "destinatario": body.comprador,
                    "evento": "PAGAMENTO_RECUSADO",
                    "mensagem": f"Pagamento recusado para o pedido {pedido_id}. Estoque liberado.",
                },
                headers=headers,
            )
            return JSONResponse(
                status_code=402,
                content={
                    "correlation_id": cid,
                    "pedido_id": pedido_id,
                    "status": "CANCELADO",
                    "compensacao_executada": True,
                    "detalhe": res_pag.json().get("detail", "Pagamento recusado"),
                },
            )

        pagamento = res_pag.json()

        # Se a transação foi idempotente (repetida), compensa a reserva extra feita no passo 1
        if pagamento.get("idempotente"):
            logger.info(
                f"cid={cid} | Pagamento idempotente detectado; revertendo reserva/pedido auxiliar"
            )
            await client.post(
                f"{CATALOGO_URL}/produtos/{body.produto_id}/liberar",
                json={"quantidade": body.quantidade},
                headers=headers,
            )
            await client.patch(
                f"{PEDIDOS_URL}/pedidos/{pedido_id}/status",
                json={"status": "CANCELADO"},
                headers=headers,
            )
            return {
                "correlation_id": cid,
                "pedido_id": pagamento["pedido_id"],
                "status": "PAGO",
                "pagamento": pagamento,
                "observacao": "Requisição idempotente: transação original reutilizada sem cobrança dupla.",
            }

        # 4. Atualizar pedido para PAGO e notificar
        await client.patch(
            f"{PEDIDOS_URL}/pedidos/{pedido_id}/status",
            json={"status": "PAGO"},
            headers=headers,
        )
        await client.post(
            f"{NOTIFICACOES_URL}/notificacoes",
            json={
                "pedido_id": pedido_id,
                "destinatario": body.comprador,
                "evento": "COMPRA_APROVADA",
                "mensagem": f"Pedido {pedido_id} aprovado ({body.metodo}) no valor de R$ {valor_total:.2f}.",
            },
            headers=headers,
        )

        logger.info(f"cid={cid} | Checkout concluído com sucesso | pedido_id={pedido_id}")
        return {
            "correlation_id": cid,
            "pedido_id": pedido_id,
            "status": "PAGO",
            "produto": dados_prod["nome"],
            "quantidade": body.quantidade,
            "valor_total": valor_total,
            "pagamento": pagamento,
        }
