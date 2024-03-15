import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide",page_title="Resultados 3º Ano B - Fund. I", page_icon="🎛")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("# Resultados 3º Ano B - Fund. I")

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
    tabela = pd.read_excel('resultados_3_ano_b.xlsx')
    return tabela

dados = carregar_dados()
media_aluno = dados.mean(axis=1)
media = dados.mean()
media_turma = media.mean().round(2)*100
conteudos1 = pd.read_excel('habilidades_fund1.xlsx')
#conteudos1
#conteudos1["Codigo"]=="EF01LP04"
#dados_filtrados = dados[conteudos1["Codigo"]=="EF01LP04"]
#dados_filtrados
dados1 = dados.assign(media=media_aluno.round(2)*100)


colors = np.ones(len(dados1['Aluno'].unique()))
colors = np.transpose(colors)
#dados_gerais = dados[dados["Learning Objective"]== 'Resultados']
index1_rec = dados1['media'] < media_turma
colors[index1_rec] = 0
dados1 = dados1.assign(colors=colors.astype('str'))

fig_geral = px.bar(dados1, x="Aluno", y="media", 
                               title=f'Notas Avaliação Diagnóstica - Geral',
                                height=800, width=1280, text_auto = True,  color="colors",
                                color_discrete_map={ '1.0': 'blue', '0.0': 'red'}
                                ).update_xaxes(categoryorder="total descending")

fig_geral.add_shape( # add a horizontal "target" line
            label_textposition="end", label_font_size=22, label_text=f'Média Geral da Turma = {media_turma} %',
            type="line", line_color="salmon", line_width=4, opacity=1, line_dash="dot",
            x0=0, x1=1, xref="paper", y0=media_turma, y1=media_turma, yref="y")
fig_geral.update(layout_showlegend=False)        
fig_geral

disciplina = st.sidebar.selectbox("Disciplina", ["Português", "Matemática"])
#dados1
habilidades = list(dados1.columns.values)[1:(-2)]
print(habilidades)
hab_port = ["Aluno"]
hab_mat = ["Aluno"]
for i in range(len(habilidades)):
    if "LP" in habilidades[i]:
        hab_port.append(habilidades[i])
    elif "MA" in habilidades[i]:
        hab_mat.append(habilidades[i])

dados_port = dados1.loc[:,  hab_port]
dados_mat = dados1.loc[:,  hab_mat]
#dados_mat

media = dados_port.mean()
media_turma_port = media.mean().round(2)*100
media = dados_mat.mean()
media_turma_mat = media.mean().round(2)*100

df_media_conteudos = pd.DataFrame([['Portugues', media_turma_port ], ['Matemática', media_turma_mat]], columns=['Conteúdos', 'Média'])
#df_media_conteudos

fig_media_conteudo = px.bar(df_media_conteudos, x="Conteúdos", y="Média", 
                               title=f'Média por Disciplina',
                                height=800, width=1280, text_auto = True, barmode='group', #color='Conteúdo',
                                ).update_xaxes(categoryorder="total descending")
        
fig_media_conteudo

if disciplina == 'Português':
    dados_plot = dados_port
elif disciplina == "Matemática":
    dados_plot = dados_mat

media_aluno = dados_plot.mean(axis=1)
media = dados_plot.mean()
media_turma = media.mean().round(2)*100
#conteudos1 = pd.read_excel('habilidades_fund1.xlsx')
#conteudos1
#conteudos1["Codigo"]=="EF01LP04"
#dados_filtrados = dados[conteudos1["Codigo"]=="EF01LP04"]
#dados_filtrados
dados1 = dados_plot.assign(media=media_aluno.round(2)*100)


colors_dis = np.ones(len(dados1['Aluno'].unique()))
colors = np.transpose(colors_dis)
media_disciplina = dados1['media'].mean().round(0)
index1_rec = dados1['media'] < media_turma
colors_dis[index1_rec] = 0
dados1 = dados1.assign(colors_dis=colors.astype('str'))
fig_disciplina = px.bar(dados1, x="Aluno", y="media", 
                               title=f'Notas Avaliação Diagnóstica - Disciplina: {disciplina}',
                                height=800, width=1280, text_auto = True, color="colors_dis",
                                color_discrete_map={ '1.0': 'blue', '0.0': 'red'}
                                ).update_xaxes(categoryorder="total descending")
fig_disciplina.add_shape( # add a horizontal "target" line
            label_textposition="end", label_font_size=22, label_text=f'Média da Turma = {media_disciplina} %',
            type="line", line_color="salmon", line_width=4, opacity=1, line_dash="dot",
            x0=0, x1=1, xref="paper", y0=media_turma, y1=media_turma, yref="y") 
fig_disciplina.update(layout_showlegend=False)    
fig_disciplina


lista = []
if disciplina == 'Português':
    for i in hab_port[1:]:
        lista.append([i, dados_port[i].mean().round(2)*100])

elif disciplina == "Matemática":
    for i in hab_mat[1:]:
        lista.append([i, dados_mat[i].mean().round(2)*100])

df_media_conteudos = pd.DataFrame(lista, columns=['Conteúdos', 'Média'])


fig_media_conteudo = px.bar(df_media_conteudos, x="Conteúdos", y="Média", 
                               title=f'Média por Habilidade - Disciplina: {disciplina}',
                                height=800, width=1280, text_auto = True, barmode='group', #color='Conteúdo',
                                ).update_xaxes(categoryorder="total descending")
        
fig_media_conteudo


if disciplina == 'Português':
    conteudo = st.selectbox("Habilidade", hab_port[1:])
elif disciplina == "Matemática":
    conteudo = st.selectbox("Habilidade", hab_mat[1:])

print(conteudo)
#conteudos1

texto_habilidade = conteudos1[conteudos1['Codigo']==conteudo]
#texto_habilidade
st.title(texto_habilidade.iloc[0,0])

fig_conteudo = px.bar(dados1, x="Aluno", y=conteudo, 
                               title=f'Notas Avaliação Diagnóstica - Disciplina: {disciplina} - {conteudo}',
                                height=800, width=1280, text_auto = True, barmode='group', #color='Condicao',
                                ).update_xaxes(categoryorder="total descending")
        
fig_conteudo

Alunos = st.selectbox("Alunos", dados1["Aluno"].sort_values().unique())

dados_aluno = dados[dados["Aluno"]==Alunos]
lista1 = []

for i in habilidades:
    lista1.append([i, int(dados_aluno[i].values)])

df_aluno = pd.DataFrame(lista1, columns=['Conteúdos', 'Nota'])

fig_aluno = px.bar(df_aluno, x="Conteúdos", y="Nota" ,
                               title=f'Notas Avaliação Diagnóstica - Aluno(a): {Alunos}',
                                height=800, width=1280, text_auto = True, barmode='group', #color='Condicao',
                                )
        
fig_aluno

lista2 = []
for i in habilidades:
    lista2.append(conteudos1["Habilidades"][conteudos1['Codigo']==i].values)

habilidades_turma = pd.DataFrame(lista2, columns=['Habilidades'])

#habilidades_turma = conteudos1[conteudos1['Codigo']==habilidades]

st.checkbox("Ampliar tabela de habilidades", value=True, key="use_container_width")
st.dataframe(habilidades_turma["Habilidades"], use_container_width=st.session_state.use_container_width)