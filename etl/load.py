import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from etl.extract import get_connection

def load_summary(df: pd.DataFrame):
    conn = get_connection()
    cursor = conn.cursor()

    records = [
        (
            int(row['usuario_id']),
            int(row['ano']),
            int(row['mes']),
            float(row['receita']),
            float(row['despesa']),
            float(row['saldo_liquido'])
        )
        for _, row in df.iterrows()
    ]

    query = """
        INSERT INTO financial_summary
            (usuario_id, ano, mes, receita, despesa, saldo_liquido)
        VALUES %s
        ON CONFLICT (usuario_id, ano, mes)
        DO UPDATE SET
            receita = EXCLUDED.receita,
            despesa = EXCLUDED.despesa,
            saldo_liquido = EXCLUDED.saldo_liquido,
            atualizado_em = CURRENT_TIMESTAMP
    """

    execute_values(cursor, query, records)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"{len(records)} registros salvos em financial_summary.")

if __name__ == "__main__":
    from etl.extract import extract_transacoes
    from etl.transform import transform

    df = extract_transacoes()
    resumo = transform(df)
    load_summary(resumo)