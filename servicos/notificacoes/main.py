import logging
import uuid
from typing import Literal
from fastapi import FastAPI, Request
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | notificacoes | %(levelname)s | %(message)s",
)
logger = logging.getLogger("notificacoes")

app = FastAPI(title="Serviço de Notificações (SOA)", version="1.0.0")

HISTORICO_NOTIFICACOES: list[dict] = []


class EnviarNotificacaoRequest(BaseModel):
    pedido_id: str
    destinatario: str
    evento: Literal["COMPRA_APROVADA", "PAGAMENTO_RECUSADO"]
    mensagem: str


def get_cid(request: Request) -> str:
    return request.headers.get("X-Correlation-ID") or str(uuid.uuid4())


@app.get("/health")
def health():
    return {"status": "ok", "servico": "notificacoes"}


@app.post("/notificacoes", status_code=201)
def enviar_notificacao(body: EnviarNotificacaoRequest, request: Request):
    cid = get_cid(request)
    registro = {
        "notificacao_id": f"notif-{uuid.uuid4().hex[:8]}",
        "pedido_id": body.pedido_id,
        "destinatario": body.destinatario,
        "evento": body.evento,
        "mensagem": body.mensagem,
    }
    HISTORICO_NOTIFICACOES.append(registro)
    logger.info(
        f"cid={cid} | Notificação enviada | evento={body.evento} "
        f"para={body.destinatario} pedido={body.pedido_id}"
    )
    return registro


@app.get("/notificacoes")
def listar_notificacoes():
    return {"total": len(HISTORICO_NOTIFICACOES), "notificacoes": HISTORICO_NOTIFICACOES}
