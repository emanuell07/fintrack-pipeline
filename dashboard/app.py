import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from api_client import get_all_summaries, get_categorias_by_usuario, get_totais_gerais 


st.set_page_config(page_title="FinTrack Dashboard", layout="wide")
st.title("📊 FinTrack — Dashboard Financeiro")

# Carrega todos os dados
data = get_all_summaries()
df = pd.DataFrame(data)
df['mes_ano'] = df['ano'].astype(str) + "-" + df['mes'].astype(str).str.zfill(2)

# Totais gerais no topo
totais = get_totais_gerais()
st.subheader("📈 Visão Geral do Sistema")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Usuários", totais['total_usuarios'])
col2.metric("Receita Total", f"R$ {totais['total_receita']:,.2f}")
col3.metric("Despesa Total", f"R$ {totais['total_despesa']:,.2f}")
col4.metric("Saldo Total", f"R$ {totais['total_saldo']:,.2f}")
st.divider()

# Tabs de navegação
tab1, tab2 = st.tabs(["👤 Por Usuário", "🏆 Comparativo Geral"])

# ─── TAB 1 — Por Usuário ───────────────────────────────────────────────
with tab1:
    st.sidebar.header("Filtros")
    usuarios = sorted(df['usuario_id'].unique())
    usuario_selecionado = st.sidebar.selectbox("Selecione o usuário", usuarios)

    anos = sorted(df['ano'].unique())
    ano_selecionado = st.sidebar.selectbox("Ano", anos, index=len(anos)-1)

    meses = sorted(df[df['ano'] == ano_selecionado]['mes'].unique())
    mes_opcoes = ["Todos"] + [str(m) for m in meses]
    mes_selecionado = st.sidebar.selectbox("Mês", mes_opcoes)

    df_usuario = df[df['usuario_id'] == usuario_selecionado]
    df_usuario = df_usuario[df_usuario['ano'] == ano_selecionado]
    if mes_selecionado != "Todos":
        df_usuario = df_usuario[df_usuario['mes'] == int(mes_selecionado)]
    df_usuario = df_usuario.sort_values('mes_ano')

    col1, col2, col3 = st.columns(3)
    saldo = df_usuario['saldo_liquido'].sum()
    col1.metric("Total Receita", f"R$ {df_usuario['receita'].sum():,.2f}")
    col2.metric("Total Despesa", f"R$ {df_usuario['despesa'].sum():,.2f}")
    col3.metric(
        "Saldo Líquido",
        f"R$ {saldo:,.2f}",
        delta=f"{'positivo' if saldo >= 0 else 'negativo'}",
        delta_color="normal" if saldo >= 0 else "inverse"
    )

    st.divider()

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

    st.subheader("Saldo Líquido por Mês")
    fig2 = px.line(
        df_usuario,
        x='mes_ano',
        y='saldo_liquido',
        markers=True,
        labels={'saldo_liquido': 'Saldo (R$)', 'mes_ano': 'Mês'},
        color_discrete_sequence=['#3498db']
    )
    fig2.add_hline(y=0, line_dash="dash", line_color="gray")
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico de pizza por categoria
    st.subheader("🍕 Gastos por Categoria")
    dados_cat = get_categorias_by_usuario(usuario_selecionado)
    df_cat = pd.DataFrame(dados_cat)

    if not df_cat.empty:
        col_pizza1, col_pizza2 = st.columns(2)

        with col_pizza1:
            df_despesa = df_cat[df_cat['tipo'] == 'despesa']
            if not df_despesa.empty:
                fig_pizza1 = px.pie(
                    df_despesa,
                    names='categoria',
                    values='total',
                    title='Despesas por Categoria',
                    color_discrete_sequence=px.colors.sequential.Reds_r
                )
                st.plotly_chart(fig_pizza1, use_container_width=True)

        with col_pizza2:
            df_receita = df_cat[df_cat['tipo'] == 'receita']
            if not df_receita.empty:
                fig_pizza2 = px.pie(
                    df_receita,
                    names='categoria',
                    values='total',
                    title='Receitas por Categoria',
                    color_discrete_sequence=px.colors.sequential.Greens_r
                )
                st.plotly_chart(fig_pizza2, use_container_width=True)

    st.subheader("Dados Detalhados")
    st.dataframe(df_usuario[['mes_ano', 'receita', 'despesa', 'saldo_liquido']], use_container_width=True)

    # Exportar CSV
    st.subheader("📥 Exportar Dados")
    csv = df_usuario[['mes_ano', 'receita', 'despesa', 'saldo_liquido']].to_csv(index=False)
    st.download_button(
        label="⬇️ Baixar CSV",
        data=csv,
        file_name=f"fintrack_usuario_{usuario_selecionado}_{ano_selecionado}.csv",
        mime="text/csv"
    )

# ─── TAB 2 — Comparativo Geral ─────────────────────────────────────────
with tab2:
    st.subheader("🏆 Ranking de Saldo Líquido por Usuário")

    df_ranking = df.groupby('usuario_id').agg(
        receita=('receita', 'sum'),
        despesa=('despesa', 'sum'),
        saldo_liquido=('saldo_liquido', 'sum')
    ).reset_index().sort_values('saldo_liquido', ascending=False)

    df_ranking['cor'] = df_ranking['saldo_liquido'].apply(
        lambda x: '#2ecc71' if x >= 0 else '#e74c3c'
    )

    fig3 = px.bar(
        df_ranking,
        x='usuario_id',
        y='saldo_liquido',
        color='cor',
        color_discrete_map='identity',
        labels={'saldo_liquido': 'Saldo Líquido (R$)', 'usuario_id': 'Usuário'},
        title="Saldo Líquido Total por Usuário"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📊 Receita x Despesa — Todos os Usuários")
    fig4 = px.bar(
        df_ranking,
        x='usuario_id',
        y=['receita', 'despesa'],
        barmode='group',
        labels={'value': 'Valor (R$)', 'usuario_id': 'Usuário'},
        color_discrete_map={'receita': '#2ecc71', 'despesa': '#e74c3c'}
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("📋 Tabela Geral")
    st.dataframe(
        df_ranking[['usuario_id', 'receita', 'despesa', 'saldo_liquido']].style.format({
            'receita': 'R$ {:,.2f}',
            'despesa': 'R$ {:,.2f}',
            'saldo_liquido': 'R$ {:,.2f}'
        }),
        use_container_width=True
    )