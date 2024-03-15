import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide",page_title="Resultados 8º Ano - Fund. II", page_icon="🎛")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("# Resultados 8º Ano - Fund. II")

def clear_submit():
    st.session_state["submit"] = False


def displayPDF(uploaded_file):
    
    # Read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')

    # Embed PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="3000" type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)


@st.cache_data
def carregar_dados():
    # tabela = pd.concat(map(pd.read_excel, glob.glob('Resultado_9ano.xlsx')))
    # tabela['ano'] = tabela['ano'].apply(lambda _: str(_))
    tabela = pd.read_excel('resultados_8_ano.xls')
    return tabela

dados = carregar_dados()
# dados
conteudos1 = pd.read_excel('Prova_8_ano.xls')
# conteudos
disciplina = st.sidebar.selectbox("Disciplina", conteudos1['Unnamed: 1'].unique())
dados_filtrados = dados[dados["Learning Objective"]== disciplina]
conteudos = conteudos1[conteudos1['Unnamed: 1'] == disciplina ]
# conteudo = st.sidebar.selectbox("Conteúdo", conteudos['Unnamed: 2'].unique())
media_geral = dados[dados["Learning Objective"]== 'Resultados']['Percent Score'].mean()
media_geral = media_geral.round(0)

colors = np.ones(len(dados_filtrados['Alunos'].unique()))
colors = np.transpose(colors)
dados_gerais = dados[dados["Learning Objective"]== 'Resultados']
index1_rec = dados_gerais['Percent Score'] < media_geral
colors[index1_rec] = 0
dados_gerais = dados_gerais.assign(colors=colors.astype('str'))

fig_geral = px.bar(dados_gerais, x="Alunos", y="Percent Score", 
                               title=f'Notas Avaliação Diagnóstica - Geral',
                                height=800, width=1280, text_auto = True,  color="colors",
                                color_discrete_map={ '1.0': 'blue', '0.0': 'red'}
                                ).update_xaxes(categoryorder="total descending")

fig_geral.add_shape( # add a horizontal "target" line
            label_textposition="end", label_font_size=22, label_text=f'Média Geral da Turma = {media_geral} %',
            type="line", line_color="salmon", line_width=4, opacity=1, line_dash="dot",
            x0=0, x1=1, xref="paper", y0=media_geral, y1=media_geral, yref="y")
fig_geral.update(layout_showlegend=False)        
fig_geral

lista_disciplinas = []
for j in conteudos1['Unnamed: 1'].unique():
    dado_disciplina = dados[dados['Learning Objective']==j]
    media = dado_disciplina['Percent Score'].mean().round(0)
    lista_disciplinas.append([j, media])

df_media_disciplinas = pd.DataFrame(lista_disciplinas, columns=['Disciplinas', 'Média'])

fig_media_disciplinas = px.bar(df_media_disciplinas, x="Disciplinas", y="Média", 
                               title=f'Média por Disciplina',
                                height=800, width=1280, text_auto = True, barmode='group', #color='Conteúdo',
                                ).update_xaxes(categoryorder="total descending")
        
fig_media_disciplinas

colors_dis = np.ones(len(dados_filtrados['Alunos'].unique()))
colors = np.transpose(colors_dis)
media_disciplina = dados_filtrados['Percent Score'].mean().round(0)
index1_rec = dados_filtrados['Percent Score'] < media_disciplina
colors_dis[index1_rec] = 0
dados_filtrados = dados_filtrados.assign(colors_dis=colors.astype('str'))
fig_disciplina = px.bar(dados_filtrados, x="Alunos", y="Percent Score", 
                               title=f'Notas Avaliação Diagnóstica - Disciplina: {disciplina}',
                                height=800, width=1280, text_auto = True, color="colors_dis",
                                color_discrete_map={ '1.0': 'blue', '0.0': 'red'}
                                ).update_xaxes(categoryorder="total descending")
fig_disciplina.add_shape( # add a horizontal "target" line
            label_textposition="end", label_font_size=22, label_text=f'Média da Turma = {media_disciplina} %',
            type="line", line_color="salmon", line_width=4, opacity=1, line_dash="dot",
            x0=0, x1=1, xref="paper", y0=media_disciplina, y1=media_disciplina, yref="y") 
fig_disciplina.update(layout_showlegend=False)    
fig_disciplina

cont = conteudos['Unnamed: 2'].unique()
lista = []
for i in cont:
    disc_conteudo = f'{disciplina} - {i}'
    print(disc_conteudo)
    teste = dados[dados["Learning Objective"]== disc_conteudo]['Percent Score'].mean()
    print(teste)
    lista.append([i, dados[dados["Learning Objective"]== disc_conteudo]['Percent Score'].mean().round(0)])
    
df_media_conteudos = pd.DataFrame(lista, columns=['Conteúdos', 'Média'])

fig_media_conteudo = px.bar(df_media_conteudos, x="Conteúdos", y="Média", 
                               title=f'Média por Conteúdo - Disciplina: {disciplina}',
                                height=800, width=1280, text_auto = True, barmode='group', #color='Conteúdo',
                                ).update_xaxes(categoryorder="total descending")
        
fig_media_conteudo


conteudo = st.selectbox("Conteúdo", conteudos['Unnamed: 2'].unique())
disc_conteudo = f'{disciplina} - {conteudo}'


fig_conteudo = px.bar(dados[dados["Learning Objective"]== disc_conteudo], x="Alunos", y="Percent Score", 
                               title=f'Notas Avaliação Diagnóstica - Disciplina: {disciplina} - {conteudo}',
                                height=800, width=1280, text_auto = True, barmode='group', #color='Condicao',
                                ).update_xaxes(categoryorder="total descending")
        
fig_conteudo


Alunos = st.selectbox("Alunos", dados["Alunos"].sort_values().unique())
dados = dados[dados["Alunos"]==Alunos]
values = conteudos1['Unnamed: 1'].unique()
# dados = dados[dados["Learning Objective"]==conteudos1['Unnamed: 1'].unique()]
media_Alunos = dados[dados["Learning Objective"]== 'Resultados']['Percent Score'].mean()
dados = dados.loc[dados["Learning Objective"].isin(values)]

fig_Alunos = px.bar(dados, x="Learning Objective", y="Percent Score", 
                               title=f'Nota do Alunos: {Alunos} por Disciplina',
                                height=800, width=1280, text_auto = True, barmode='group', #color='Conteúdo',
                                ).update_xaxes(categoryorder="total descending")
fig_Alunos.add_shape( # add a horizontal "target" line
            label_textposition="end", label_font_size=22, label_text=f'Média do Alunos = {media_Alunos} %',
            type="line", line_color="salmon", line_width=4, opacity=1, line_dash="dot",
            x0=0, x1=1, xref="paper", y0=media_Alunos, y1=media_Alunos, yref="y")         
fig_Alunos


