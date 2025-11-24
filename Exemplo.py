import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard de Vendas Sintético", layout="wide")

# --- FUNÇÃO GERADORA DE DADOS (SIMULA O BANCO) ---
# O decorador @st.cache_data impede que os dados mudem a cada interação simples
@st.cache_data
def gerar_dados_sinteticos(n_linhas):
    produtos = ['Notebook', 'Smartphone', 'Monitor', 'Mouse', 'Teclado', 'Webcam']
    categorias = ['Eletrônicos', 'Acessórios', 'Periféricos']
    regioes = ['Sul', 'Sudeste', 'Norte', 'Nordeste', 'Centro-Oeste']
    
    dados = []
    data_inicial = datetime(2024, 1, 1)
    
    for _ in range(n_linhas):
        produto = random.choice(produtos)
        categoria = categorias[0] if produto in ['Notebook', 'Smartphone'] else (categorias[2] if produto in ['Mouse', 'Teclado'] else 'Acessórios')
        
        linha = {
            'Data': data_inicial + timedelta(days=random.randint(0, 365)),
            'Produto': produto,
            'Categoria': categoria,
            'Região': random.choice(regioes),
            'Qtd': random.randint(1, 20),
            'Preço Unitário': round(random.uniform(50.0, 4500.0), 2),
        }
        linha['Total Venda'] = linha['Qtd'] * linha['Preço Unitário']
        dados.append(linha)
        
    return pd.DataFrame(dados)

# --- BARRA LATERAL (CONTROLES) ---
st.sidebar.header("1. Configuração do Banco")
n_linhas = st.sidebar.slider("Tamanho do Banco de Dados (linhas)", 100, 5000, 1000)
btn_gerar = st.sidebar.button("Gerar Novos Dados Aleatórios")

# Se clicar no botão, limpamos o cache para forçar nova geração
if btn_gerar:
    st.cache_data.clear()

# Carrega os dados
df = gerar_dados_sinteticos(n_linhas)

st.sidebar.markdown("---")
st.sidebar.header("2. Filtros de Análise")

# Filtro de Região
filtro_regiao = st.sidebar.multiselect(
    "Filtrar Região:", 
    options=df['Região'].unique(),
    default=df['Região'].unique()
)

# Filtro de Categoria
filtro_categoria = st.sidebar.multiselect(
    "Filtrar Categoria:",
    options=df['Categoria'].unique(),
    default=df['Categoria'].unique()
)

# --- APLICAÇÃO DOS FILTROS ---
df_filtrado = df[
    (df['Região'].isin(filtro_regiao)) & 
    (df['Categoria'].isin(filtro_categoria))
]

# --- DASHBOARD PRINCIPAL ---
st.title("📊 Dashboard de Vendas (Dados Sintéticos)")

# Métricas (KPIs)
total_faturamento = df_filtrado['Total Venda'].sum()
total_vendas = df_filtrado['Qtd'].sum()
ticket_medio = df_filtrado['Total Venda'].mean() if not df_filtrado.empty else 0

col1, col2, col3 = st.columns(3)
col1.metric("Faturamento Total", f"R$ {total_faturamento:,.2f}")
col2.metric("Itens Vendidos", f"{total_vendas}")
col3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.markdown("---")

# Gráficos e Tabelas
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Vendas por Produto")
    # Agrupamento simples para o gráfico
    vendas_produto = df_filtrado.groupby('Produto')['Total Venda'].sum().sort_values(ascending=False)
    st.bar_chart(vendas_produto)

with col_graf2:
    st.subheader("Evolução Temporal")
    # Agrupamento por data
    vendas_tempo = df_filtrado.groupby('Data')['Total Venda'].sum()
    st.line_chart(vendas_tempo)

# Tabela Detalhada
with st.expander("Visualizar Base de Dados Filtrada"):
    st.dataframe(
        df_filtrado.sort_values(by='Data', ascending=False),
        use_container_width=True,
        hide_index=True
    )
    st.caption(f"Mostrando {len(df_filtrado)} registros de {len(df)} gerados.")
