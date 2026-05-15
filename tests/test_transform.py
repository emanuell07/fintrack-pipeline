import pytest
import pandas as pd
from etl.extract import extract_transacoes
from etl.transform import transform

@pytest.fixture
def df_transformado():
    df = extract_transacoes()
    return transform(df)

def test_transform_retorna_dados(df_transformado):
    assert df_transformado is not None
    assert len(df_transformado) > 0

def test_transform_colunas(df_transformado):
    colunas_esperadas = ['usuario_id', 'ano', 'mes', 'receita', 'despesa', 'saldo_liquido']
    for coluna in colunas_esperadas:
        assert coluna in df_transformado.columns, f"Coluna '{coluna}' não encontrada"

def test_transform_saldo_liquido(df_transformado):
    saldo_calculado = (df_transformado['receita'] - df_transformado['despesa']).round(2)
    saldo_real = df_transformado['saldo_liquido'].round(2)
    assert (saldo_calculado == saldo_real).all(), "Saldo líquido calculado incorretamente"

def test_transform_valores_nao_negativos(df_transformado):
    assert (df_transformado['receita'] >= 0).all(), "Existem receitas negativas"
    assert (df_transformado['despesa'] >= 0).all(), "Existem despesas negativas"