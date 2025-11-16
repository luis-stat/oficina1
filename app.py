import streamlit as st
import pandas as pd

st.title("Dashboard Exploratório da Pesquisa")

def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        cols_numericas = ['horas_estudo_semanal', 'tempo_deslocamento_min', 'semestre', 'nivel_disposição_pos_aula']
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
    
    st.write(f"Total de alunos filtrados: {len(df_filtrado)}")
    st.dataframe(df_filtrado)
else:
    st.error("Arquivo 'dados.csv' não encontrado.")