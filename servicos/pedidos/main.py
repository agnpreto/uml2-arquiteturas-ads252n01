import logging
import uuid
from typing import Literal
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | pedidos | %(levelname)s | %(message)s",
)
logger = logging.getLogger("pedidos")

app = FastAPI(title="Serviço de Pedidos (SOA)", version="1.0.0")

PEDIDOS: dict[str, dict] = {}


class CriarPedidoRequest(BaseModel):
    comprador: str
    produto_id: str
    quantidade: int = Field(gt=0)
    valor_total: float = Field(gt=0)
    vendedor_id: str


class AtualizarStatusRequest(BaseModel):
    status: Literal["PENDENTE", "PAGO", "CANCELADO"]


def get_cid(request: Request) -> str:
    return request.headers.get("X-Correlation-ID") or str(uuid.uuid4())


@app.get("/health")
def health():
    return {"status": "ok", "servico": "pedidos"}


@app.post("/pedidos", status_code=201)
def criar_pedido(body: CriarPedidoRequest, request: Request):
    cid = get_cid(request)
    pedido_id = f"ped-{uuid.uuid4().hex[:8]}"
    pedido = {
        "pedido_id": pedido_id,
        "comprador": body.comprador,
        "produto_id": body.produto_id,
        "quantidade": body.quantidade,
        "valor_total": round(body.valor_total, 2),
        "vendedor_id": body.vendedor_id,
        "status": "PENDENTE",
    }
    PEDIDOS[pedido_id] = pedido
    logger.info(
        f"cid={cid} | Pedido criado | pedido_id={pedido_id} status=PENDENTE "
        f"valor={pedido['valor_total']}"
    )
    return pedido


@app.patch("/pedidos/{pedido_id}/status")
def atualizar_status(pedido_id: str, body: AtualizarStatusRequest, request: Request):
    cid = get_cid(request)
    pedido = PEDIDOS.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    status_anterior = pedido["status"]
    pedido["status"] = body.status
    logger.info(
        f"cid={cid} | Status atualizado | pedido_id={pedido_id} "
        f"{status_anterior} -> {body.status}"
    )
    return pedido


@app.get("/pedidos/{pedido_id}")
def obter_pedido(pedido_id: str):
    pedido = PEDIDOS.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido
