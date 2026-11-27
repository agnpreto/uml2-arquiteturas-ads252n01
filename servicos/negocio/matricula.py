from flask import Blueprint, request, jsonify
from db import conectar

matricula_bp = Blueprint("matricula", __name__)


def resposta(status, mensagem, codigo=200):
    return jsonify({"status": status, "mensagem": mensagem}), codigo


@matricula_bp.route("/matricula", methods=["POST"])
def matricular():
    dados = request.get_json(silent=True) or {}
    aluno_id = dados.get("aluno_id")
    disciplina_id = dados.get("disciplina_id")
    if not aluno_id or not disciplina_id:
        return resposta("erro", "Informe aluno_id e disciplina_id.", 400)
    conn = conectar()
    try:
        return efetivar_matricula(conn, aluno_id, disciplina_id)
    finally:
        conn.close()

def validar_matricula(cur, aluno_id, disciplina_id):
    """Devolve uma mensagem de erro, ou None se estiver tudo certo."""
    cur.execute("SELECT 1 FROM alunos WHERE id = %s", (aluno_id,))
    if cur.fetchone() is None:
        return "Aluno não encontrado."

    cur.execute("SELECT vagas FROM disciplinas WHERE id = %s", (disciplina_id,))
    linha = cur.fetchone()
    if linha is None:
        return "Disciplina não encontrada."
    if linha[0] <= 0:
        return "Não há vagas nesta disciplina."

    cur.execute(
        "SELECT 1 FROM matriculas WHERE aluno_id = %s AND disciplina_id = %s",
        (aluno_id, disciplina_id),
    )
    if cur.fetchone() is not None:
        return "Você já está matriculado nesta disciplina."
    return None

def efetivar_matricula(conn, aluno_id, disciplina_id):
    cur = conn.cursor()
    erro = validar_matricula(cur, aluno_id, disciplina_id)
    if erro:
        print(f"[NEGOCIO] Matricula recusada: aluno={aluno_id} disciplina={disciplina_id} motivo={erro}", flush=True)
        return resposta("erro", erro, 409)

    cur.execute(
        "INSERT INTO matriculas (aluno_id, disciplina_id) VALUES (%s, %s)",
        (aluno_id, disciplina_id),
    )
    cur.execute("UPDATE disciplinas SET vagas = vagas - 1 WHERE id = %s", (disciplina_id,))
    conn.commit()
    print(f"[NEGOCIO] Matricula confirmada: aluno={aluno_id} disciplina={disciplina_id}", flush=True)
    return resposta("ok", "Matrícula confirmada!")


@matricula_bp.route("/matriculas/<int:aluno_id>", methods=["GET"])
def consultar_matriculas(aluno_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        """SELECT d.id, d.nome
           FROM matriculas m
           JOIN disciplinas d ON d.id = m.disciplina_id
           WHERE m.aluno_id = %s
           ORDER BY d.nome""",
        (aluno_id,),
    )
    linhas = cur.fetchall()
    conn.close()
    return jsonify([{"id": l[0], "nome": l[1]} for l in linhas])
