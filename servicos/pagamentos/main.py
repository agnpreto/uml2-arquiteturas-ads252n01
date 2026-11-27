import logging
import uuid
from typing import Literal
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | pagamentos | %(levelname)s | %(message)s",
)
logger = logging.getLogger("pagamentos")

app = FastAPI(title="Serviço de Pagamentos e Split (SOA)", version="1.0.0")

TRANSACOES_POR_CHAVE: dict[str, dict] = {}
TAXA_MARKETPLACE = 0.10


class ProcessarPagamentoRequest(BaseModel):
    pedido_id: str
    vendedor_id: str
    valor: float = Field(gt=0)
    metodo: Literal["PIX", "CARTAO"]
    idempotency_key: str
    simular_falha: bool = False


def get_cid(request: Request) -> str:
    return request.headers.get("X-Correlation-ID") or str(uuid.uuid4())


@app.get("/health")
def health():
    return {"status": "ok", "servico": "pagamentos"}


@app.post("/pagamentos")
def processar_pagamento(body: ProcessarPagamentoRequest, request: Request):
    cid = get_cid(request)

    if body.idempotency_key in TRANSACOES_POR_CHAVE:
        existente = TRANSACOES_POR_CHAVE[body.idempotency_key]
        logger.info(
            f"cid={cid} | IDEMPOTÊNCIA ATIVADA | key={body.idempotency_key} "
            f"transacao={existente['transacao_id']} (sem cobrança duplicada)"
        )
        return {**existente, "idempotente": True}

    if body.simular_falha:
        logger.warning(
            f"cid={cid} | Pagamento RECUSADO | pedido_id={body.pedido_id} "
            f"metodo={body.metodo} valor={body.valor:.2f}"
        )
        raise HTTPException(
            status_code=402,
            detail="Pagamento recusado pelo provedor financeiro",
        )

    comissao_marketplace = round(body.valor * TAXA_MARKETPLACE, 2)
    repasse_vendedor = round(body.valor - comissao_marketplace, 2)

    transacao = {
        "transacao_id": f"tx-{uuid.uuid4().hex[:8]}",
        "pedido_id": body.pedido_id,
        "vendedor_id": body.vendedor_id,
        "metodo": body.metodo,
        "valor_total": round(body.valor, 2),
        "split": {
            "marketplace_comissao_10pct": comissao_marketplace,
            "vendedor_repasse_90pct": repasse_vendedor,
        },
        "status": "APROVADO",
        "idempotency_key": body.idempotency_key,
        "idempotente": False,
    }
    TRANSACOES_POR_CHAVE[body.idempotency_key] = transacao

    logger.info(
        f"cid={cid} | Pagamento APROVADO | tx={transacao['transacao_id']} "
        f"pedido={body.pedido_id} total={transacao['valor_total']:.2f} "
        f"split(mkt={comissao_marketplace:.2f}, vend={repasse_vendedor:.2f})"
    )
    return transacao
