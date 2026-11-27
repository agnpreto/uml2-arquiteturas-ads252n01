
from flask import Blueprint, jsonify
from db import conectar

disciplinas_bp = Blueprint("disciplinas", __name__)

@disciplinas_bp.route("/disciplinas", methods=["GET"])
def listar_disciplinas():
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, vagas
            FROM disciplinas
            ORDER BY id
        """)

        resultados = cursor.fetchall()

        disciplinas = [
            {
                "id": linha[0],
                "nome": linha[1],
                "vagas": linha[2]
            }
            for linha in resultados
        ]

        return jsonify(disciplinas), 200

    except Exception:
        return jsonify({
            "erro": "Erro ao consultar disciplinas"
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
