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
    st.write("Dados Brutos:")
    st.dataframe(df)
else:
    st.error("Arquivo 'dados.csv' não encontrado.")