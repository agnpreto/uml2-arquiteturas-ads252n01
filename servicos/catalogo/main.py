import logging
import uuid
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | catalogo | %(levelname)s | %(message)s",
)
logger = logging.getLogger("catalogo")

app = FastAPI(title="Serviço de Catálogo e Vendedores (SOA)", version="1.0.0")

PRODUTOS = {
    "prod-1": {
        "id": "prod-1",
        "nome": "Teclado Mecânico RGB",
        "preco": 250.00,
        "estoque": 10,
        "vendedor_id": "vend-techstore",
    },
    "prod-2": {
        "id": "prod-2",
        "nome": "Mouse Gamer Sem Fio",
        "preco": 180.00,
        "estoque": 5,
        "vendedor_id": "vend-perifericos",
    },
}


class MovimentacaoEstoque(BaseModel):
    quantidade: int = Field(gt=0)


def get_cid(request: Request) -> str:
    return request.headers.get("X-Correlation-ID") or str(uuid.uuid4())


@app.get("/health")
def health():
    return {"status": "ok", "servico": "catalogo"}


@app.get("/produtos")
def listar_produtos(request: Request):
    cid = get_cid(request)
    logger.info(f"cid={cid} | Listando {len(PRODUTOS)} produtos do catálogo")
    return {"produtos": list(PRODUTOS.values())}


@app.get("/produtos/{produto_id}")
def obter_produto(produto_id: str, request: Request):
    cid = get_cid(request)
    produto = PRODUTOS.get(produto_id)
    if not produto:
        logger.warning(f"cid={cid} | Produto {produto_id} não encontrado")
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    logger.info(f"cid={cid} | Consulta produto={produto_id} estoque={produto['estoque']}")
    return produto


@app.post("/produtos/{produto_id}/reservar")
def reservar_estoque(produto_id: str, body: MovimentacaoEstoque, request: Request):
    cid = get_cid(request)
    produto = PRODUTOS.get(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    if produto["estoque"] < body.quantidade:
        logger.warning(
            f"cid={cid} | Estoque insuficiente para {produto_id}: "
            f"solicitado={body.quantidade} disponivel={produto['estoque']}"
        )
        raise HTTPException(status_code=409, detail="Estoque insuficiente")

    produto["estoque"] -= body.quantidade
    logger.info(
        f"cid={cid} | Estoque reservado | produto={produto_id} qtd={body.quantidade} "
        f"restante={produto['estoque']}"
    )
    return {
        "produto_id": produto_id,
        "nome": produto["nome"],
        "preco_unitario": produto["preco"],
        "vendedor_id": produto["vendedor_id"],
        "estoque_restante": produto["estoque"],
    }


@app.post("/produtos/{produto_id}/liberar")
def liberar_estoque(produto_id: str, body: MovimentacaoEstoque, request: Request):
    cid = get_cid(request)
    produto = PRODUTOS.get(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto["estoque"] += body.quantidade
    logger.info(
        f"cid={cid} | COMPENSAÇÃO: Estoque liberado | produto={produto_id} "
        f"qtd={body.quantidade} estoque_atual={produto['estoque']}"
    )
    return {"produto_id": produto_id, "estoque_atual": produto["estoque"]}
