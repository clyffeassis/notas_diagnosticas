import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide", page_title="Meu Site Streamlit")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


with st.container():
    #st.subheader("Meu primeiro site com o Streamlit")
    st.title("Dashboard de Notas")
    st.write("Informações sobre notas dos Aluno das avaliações dianósticas.")
    st.write("Navegue no menu do lado esquerdo para visualizar os dados.")