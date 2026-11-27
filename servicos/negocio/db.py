
import os
import psycopg2


def conectar():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "banco"),
        dbname=os.environ.get("DB_NAME", "academico"),
        user=os.environ.get("DB_USER", "academico"),
        password=os.environ.get("DB_PASSWORD", "academico")
    )
