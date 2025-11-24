import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm

st.set_page_config(page_title="Dashboard Exploratório", layout="wide")
st.title("Análises do tempo de deslocamento dos estudantes da UFC")

@st.cache_data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        cols_numericas = ['horas_estudo_semanal', 'tempo_deslocamento_min', 'semestre', 'nivel_disposicao_pos_aula']
        for col in cols_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df.dropna(subset=cols_numericas)
    except FileNotFoundError:
        return None

df = load_data("dados.csv")

if df is not None:
    st.sidebar.header("Filtros")
    
    opcoes_cursos = ["Todos"] + list(df['curso'].unique())
    curso_selecionado = st.sidebar.selectbox("Curso:", options=opcoes_cursos)

    min_sem, max_sem = int(df['semestre'].min()), int(df['semestre'].max())
    faixa_semestre = st.sidebar.slider(
        "Semestres:",
        min_value=min_sem,
        max_value=max_sem,
        value=(min_sem, max_sem)
    )

    df_filtrado = df.copy()

    if curso_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['curso'] == curso_selecionado]

    df_filtrado = df_filtrado[
        (df_filtrado['semestre'] >= faixa_semestre[0]) & 
        (df_filtrado['semestre'] <= faixa_semestre[1])
    ]
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric("Total de Alunos", f"{len(df_filtrado)}")
    with col_kpi2:
        media_estudo = df_filtrado['horas_estudo_semanal'].mean()
        st.metric("Média Horas de Estudo", f"{media_estudo:.1f} h")
    with col_kpi3:
        media_desloc = df_filtrado['tempo_deslocamento_min'].mean()
        st.metric("Média Deslocamento", f"{media_desloc:.1f} min")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição dos Dados")
        var_analise = st.selectbox("Variável:", options=['horas_estudo_semanal', 'tempo_deslocamento_min', 'nivel_disposicao_pos_aula'])
        fig_hist = px.histogram(df_filtrado, x=var_analise, nbins=20, title=f"Histograma: {var_analise}")
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        st.subheader("Relação: Deslocamento vs. Estudo")
        fig_scatter = px.scatter(
            df_filtrado, x='tempo_deslocamento_min', y='horas_estudo_semanal',
            color='curso', size='horas_estudo_semanal', trendline="ols"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with st.expander("Visualizar Dados"):
        st.dataframe(df_filtrado)
else:
    st.error("Arquivo 'dados.csv' não encontrado.")