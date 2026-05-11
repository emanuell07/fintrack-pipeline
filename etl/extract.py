import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def extract_transacoes() -> pd.DataFrame:
    conn = get_connection()
    query = """
        SELECT
            t.id,
            t.conta_id,
            t.categoria_id,
            t.descricao,
            t.valor,
            t.tipo,
            t.data_transacao,
            c.usuario_id,
            cat.nome AS categoria_nome
        FROM transacoes t
        JOIN contas c ON t.conta_id = c.id
        JOIN categorias cat ON t.categoria_id = cat.id
        ORDER BY t.data_transacao
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def extract_usuarios() -> pd.DataFrame:
    conn = get_connection()
    query = """
        SELECT id, nome, email, cidade
        FROM usuarios
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def extract_contas() -> pd.DataFrame:
    conn = get_connection()
    query = """
        SELECT id, usuario_id, tipo, saldo_inicial
        FROM contas
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    df = extract_transacoes()
    print(df)