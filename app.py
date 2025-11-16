import streamlit as st
import pandas as pd

st.title("Dashboard Exploratório da Pesquisa")

def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        return None

df = load_data("dados.csv")

if df is not None:
    st.write("Dados Brutos:")
    st.dataframe(df)
else:
    st.error("Arquivo 'dados.csv' não encontrado.")