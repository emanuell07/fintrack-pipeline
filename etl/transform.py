import pandas as pd

def transform(df_transacoes: pd.DataFrame) -> pd.DataFrame:
    df = df_transacoes.copy()

    # Garante tipos corretos
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    df['data_transacao'] = pd.to_datetime(df['data_transacao'])

    # Extrai ano e mês
    df['ano'] = df['data_transacao'].dt.year
    df['mes'] = df['data_transacao'].dt.month

    # Agrupa por usuário, ano, mês e tipo
    resumo = df.groupby(['usuario_id', 'ano', 'mes', 'tipo'])['valor'].sum().reset_index()
    resumo.columns = ['usuario_id', 'ano', 'mes', 'tipo', 'total']

    # Pivota receita x despesa lado a lado
    pivot = resumo.pivot_table(
        index=['usuario_id', 'ano', 'mes'],
        columns='tipo',
        values='total',
        fill_value=0
    ).reset_index()

    pivot.columns.name = None

    # Garante que as colunas existem mesmo se não houver dados
    for col in ['receita', 'despesa']:
        if col not in pivot.columns:
            pivot[col] = 0

    # Calcula saldo líquido
    pivot['saldo_liquido'] = pivot['receita'] - pivot['despesa']

    return pivot

if __name__ == "__main__":
    from etl.extract import extract_transacoes
    df = extract_transacoes()
    resultado = transform(df)
    print(resultado)