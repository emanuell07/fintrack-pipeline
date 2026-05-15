import streamlit as st
import plotly.express as px
import pandas as pd
from api_client import get_all_summaries, get_summary_by_usuario

st.set_page_config(page_title="FinTrack Dashboard", layout="wide")
st.title("📊 FinTrack — Dashboard Financeiro")

# Carrega todos os dados
data = get_all_summaries()
df = pd.DataFrame(data)
df['mes_ano'] = df['ano'].astype(str) + "-" + df['mes'].astype(str).str.zfill(2)

# Sidebar — filtro por usuário
st.sidebar.header("Filtros")
usuarios = sorted(df['usuario_id'].unique())
usuario_selecionado = st.sidebar.selectbox("Selecione o usuário", usuarios)

# Filtra dados do usuário
df_usuario = df[df['usuario_id'] == usuario_selecionado].sort_values('mes_ano')

# Métricas gerais
col1, col2, col3 = st.columns(3)
col1.metric("Total Receita", f"R$ {df_usuario['receita'].sum():,.2f}")
col2.metric("Total Despesa", f"R$ {df_usuario['despesa'].sum():,.2f}")
col3.metric("Saldo Líquido", f"R$ {df_usuario['saldo_liquido'].sum():,.2f}")

st.divider()

# Gráfico receita x despesa
st.subheader(f"Receita x Despesa — Usuário {usuario_selecionado}")
fig1 = px.bar(
    df_usuario,
    x='mes_ano',
    y=['receita', 'despesa'],
    barmode='group',
    labels={'value': 'Valor (R$)', 'mes_ano': 'Mês'},
    color_discrete_map={'receita': '#2ecc71', 'despesa': '#e74c3c'}
)
st.plotly_chart(fig1, use_container_width=True)

# Gráfico saldo líquido
st.subheader("Saldo Líquido por Mês")
fig2 = px.line(
    df_usuario,
    x='mes_ano',
    y='saldo_liquido',
    markers=True,
    labels={'saldo_liquido': 'Saldo (R$)', 'mes_ano': 'Mês'},
    color_discrete_sequence=['#3498db']
)
st.plotly_chart(fig2, use_container_width=True)

# Tabela de dados
st.subheader("Dados Detalhados")
st.dataframe(df_usuario[['mes_ano', 'receita', 'despesa', 'saldo_liquido']], use_container_width=True)