import pytest
from etl.extract import extract_transacoes, extract_usuarios, extract_contas

def test_extract_transacoes_retorna_dados():
    df = extract_transacoes()
    assert df is not None
    assert len(df) > 0

def test_extract_transacoes_colunas():
    df = extract_transacoes()
    colunas_esperadas = ['id', 'conta_id', 'categoria_id', 'descricao', 'valor', 'tipo', 'data_transacao', 'usuario_id', 'categoria_nome']
    for coluna in colunas_esperadas:
        assert coluna in df.columns, f"Coluna '{coluna}' não encontrada"

def test_extract_transacoes_tipos_validos():
    df = extract_transacoes()
    tipos_validos = ['receita', 'despesa']
    assert df['tipo'].isin(tipos_validos).all(), "Existem tipos inválidos nas transações"

def test_extract_usuarios_retorna_dados():
    df = extract_usuarios()
    assert df is not None
    assert len(df) > 0

def test_extract_contas_retorna_dados():
    df = extract_contas()
    assert df is not None
    assert len(df) > 0