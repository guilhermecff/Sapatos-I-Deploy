import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title='Dashboard Paula Torres', page_icon='📊', layout='wide')

# Centralizar e ampliar o título
st.markdown(
    """
    <h1 style='text-align: center; font-size: 80px;'>Dashboard Paula Torres 📊</h1>
    """,
    unsafe_allow_html=True
)

# Ocultar estilo padrão do Streamlit
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Carregar dados
data_whats = pd.read_csv('Sapatos 1- Formulário de Pesquisa Externo Whats_August 6, 2024_14.04.csv')
data_netquest = pd.read_csv('Sapatos 1- Formulário de Pesquisa Externo Qualtrics_August 6, 2024_13.42.csv')
data_interno = pd.read_csv('Sapatos 1- Formulário de Pesquisa Interno_August 6, 2024_14.04.csv')

data_whats = data_whats.iloc[:, 17:]
data_whats = data_whats.drop([0, 1])
data_whats = data_whats.dropna(thresh=10)
data_whats['Tipo'] = 'Whatsapp'

data_whats['Q34'] = data_whats['Q34'].fillna(data_whats['Como conheceu'])
data_whats = data_whats.drop(columns=['Como conheceu'])

data_whats['Q45_1'] = data_whats['Q45_1'].fillna(data_whats['Classificação_1'])
data_whats['Q45_2'] = data_whats['Q45_2'].fillna(data_whats['Classificação_2'])
data_whats['Q45_3'] = data_whats['Q45_3'].fillna(data_whats['Classificação_3'])
data_whats['Q45_4'] = data_whats['Q45_4'].fillna(data_whats['Classificação_4'])
data_whats['Q45_5'] = data_whats['Q45_5'].fillna(data_whats['Classificação_5'])
data_whats = data_whats.drop(columns=['Classificação_1', 'Classificação_2', 'Classificação_3', 'Classificação_4', 'Classificação_5'])

data_whats['Q30'] = data_whats['Q30'].fillna(data_whats['Q44'])
data_whats = data_whats.drop(columns=['Q44'])
data_whats = data_whats.rename(columns={'Q30': 'Canal Influencia'})

data_whats['Procura'] = data_whats['Procura'].fillna(data_whats['Q42'])
data_whats = data_whats.drop(columns=['Q42'])

data_netquest = data_netquest.iloc[:, 17:]
data_netquest = data_netquest.drop([0, 1])
data_netquest = data_netquest.drop(columns='ticket')
data_netquest = data_netquest.dropna(thresh=10)
data_netquest['Tipo'] = 'Pesquisa Externa Netquest'
data_netquest = data_netquest.rename(columns={'idade': 'Idade', 'reg':'Região'})
data_netquest = data_netquest.rename(columns={'sel':'Classe'})

data_netquest['Q34'] = data_netquest['Q34'].fillna(data_netquest['Como conheceu'])
data_netquest = data_netquest.drop(columns=['Como conheceu'])

data_netquest['Q45_1'] = data_netquest['Q45_1'].fillna(data_netquest['Classificação_1'])
data_netquest['Q45_2'] = data_netquest['Q45_2'].fillna(data_netquest['Classificação_2'])
data_netquest['Q45_3'] = data_netquest['Q45_3'].fillna(data_netquest['Classificação_3'])
data_netquest['Q45_4'] = data_netquest['Q45_4'].fillna(data_netquest['Classificação_4'])
data_netquest['Q45_5'] = data_netquest['Q45_5'].fillna(data_netquest['Classificação_5'])
data_netquest = data_netquest.drop(columns=['Classificação_1', 'Classificação_2', 'Classificação_3', 'Classificação_4', 'Classificação_5'])

data_netquest['Q30'] = data_netquest['Q30'].fillna(data_netquest['Q44'])
data_netquest = data_netquest.drop(columns=['Q44'])
data_netquest = data_netquest.rename(columns={'Q30': 'Canal Influencia'})

data_netquest['Procura'] = data_netquest['Procura'].fillna(data_netquest['Q42'])
data_netquest = data_netquest.drop(columns=['Q42'])

mapa = {'1': 'Classe A', '2': 'Classe B', '3': 'Classe B', '4': 'Classe C', '5': 'Classe C'}

data_netquest['Classe'] = data_netquest['Classe'].map(mapa)

faixas_etarias = {
    '18 a 24 anos': (18, 24),
    '25 a 34 anos': (25, 34),
    '35 a 44 anos': (35, 44),
    '45 a 54 anos': (45, 54),
    '55 a 64 anos': (55, 100)
}

def converter_para_faixa(idade):
    if isinstance(idade, str) and idade.isdigit():
        idade = int(idade)  
        
        for faixa, (inicio, fim) in faixas_etarias.items():
            if inicio <= idade <= fim:
                return faixa

data_netquest['Idade'] = data_netquest['Idade'].apply(converter_para_faixa)

data_interno = data_interno.iloc[:, 17:]
data_interno = data_interno.drop([0, 1])
data_interno = data_interno.dropna(thresh=10)
data_interno['É consumidor'] = 'Sim'
data_interno['Tipo'] = 'Pesquisa Interna'
data_interno = data_interno.rename(columns={'Q53': 'Q40', 'Q54':'Q41', 'Q30':'Canal Influencia'})

data_whats = data_whats.reset_index(drop=True)
data_netquest = data_netquest.reset_index(drop=True)
data_interno = data_interno.reset_index(drop=True)

mapeamento_regiao = {
    'Centro-Oeste': 'Centro-Oeste',
    'Nordeste': 'Nordeste',
    'Norte': 'Norte',
    'Sudeste': 'Sudeste',
    'Sul': 'Sul',
    '5': 'Centro-Oeste',
    '4': 'Sul',
    '3': 'Sudeste'
}

data_all = pd.concat([data_whats, data_netquest, data_interno], axis=0)
data_all['Região'] = data_all['Região'].map(mapeamento_regiao)
data_all = data_all.dropna(subset=['Idade'])
data_all = data_all[data_all['Marcas'].str.contains('Paula Torres', na=False)]

# Função para criar gráficos de barras com Plotly
def create_bar_chart(data, title, xlabel, ylabel, xtick_rotation=0, color='#d33682'):
    if data.empty:
        st.markdown(f"**{title}**: Sem dados para exibir.")
        return None

    fig = px.bar(
        data,
        x=data.index,
        y=data.values,
        title=title,
        labels={'index': xlabel, 'value': ylabel},
        color_discrete_sequence=[color]
    )
    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        title_font=dict(size=20),
        plot_bgcolor='white',  # Ajuste para fundo branco
        paper_bgcolor='white',  # Ajuste para fundo branco
        font=dict(color='black'),  # Texto em preto para melhor contraste
        xaxis=dict(tickangle=xtick_rotation),
        yaxis=dict(showgrid=False)
    )
    fig.update_xaxes(tickangle=xtick_rotation, tickfont=dict(size=14), color='black', showgrid=False)
    fig.update_yaxes(tickfont=dict(size=14), color='black')
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Quantidade: %{y}<extra></extra>'
    )
    return fig

# Sidebar para seleção de filtros
formulario_selecionado = st.sidebar.multiselect('Escolha um formulário:', options=data_all['Tipo'].unique(), default=data_all['Tipo'].unique())
consumidor_selecionado = st.sidebar.multiselect('É consumidor:', options=data_all['É consumidor'].unique(), default=data_all['É consumidor'].unique())
faixas_etarias_selecionadas = st.sidebar.multiselect('Escolha faixas etárias:', options=data_all['Idade'].unique(), default=data_all['Idade'].unique())
regioes_selecionadas = st.sidebar.multiselect('Escolha regiões:', options=data_all['Região'].unique(), default=data_all['Região'].unique())
locais_selecionados = st.sidebar.multiselect('Escolha lugares:', options=data_all['Lugar'].unique(), default=data_all['Lugar'].unique())
frequencias_selecionadas = st.sidebar.multiselect('Escolha frequências:', options=data_all['Frequência'].unique(), default=data_all['Frequência'].unique())

# Filtrar dados com base nos atributos selecionados
dados_filtrados = data_all[
    (data_all['Idade'].isin(faixas_etarias_selecionadas)) &
    (data_all['Região'].isin(regioes_selecionadas)) &
    (data_all['Lugar'].isin(locais_selecionados)) &
    (data_all['Frequência'].isin(frequencias_selecionadas)) &
    (data_all['Tipo'].isin(formulario_selecionado)) &
    (data_all['É consumidor'].isin(consumidor_selecionado))
]

# Mapear faixas etárias para valores numéricos
age_mapping = {
    '18 a 24 anos': 21,
    '25 a 34 anos': 29.5,
    '35 a 44 anos': 39.5,
    '45 a 54 anos': 49.5,
    '55 a 64 anos': 59.5,
}

dados_filtrados['Idade_Num'] = dados_filtrados['Idade'].map(age_mapping)

# Definir mapeamentos para categorias
mapeamento_classe = {
    'Classe A: Renda familiar acima de R$ 11.262 por mês.': 'Classe A',
    'Classe C: Renda familiar entre R$ 2.005 e R$ 8.640 por mês.': 'Classe C',
    'Classe B: Renda familiar entre R$ 8.641 e R$ 11.261 por mês.': 'Classe B'
}
dados_filtrados['Classe'] = dados_filtrados['Classe'].map(mapeamento_classe)

mapemamento = {
    'Lojas físicas': 'Loja Física',
    'Ambos na mesma proporção': 'Mesma proporção',
    'Online': 'Loja Online'
}

dados_filtrados['Lugar'] = dados_filtrados['Lugar'].map(mapemamento)

mapemamento = {
    'Redes sociais': 'Redes Sociais',
    'Loja física': 'Loja Física',
    'Recomendação de amigos/família': 'Recomendação',
    'Outro': 'Outro',
    'Colaborações com outras marcas': 'Colaboração',
}

dados_filtrados['Q34'] = dados_filtrados['Q34'].map(mapemamento)

mapemamento = {
    '1 ou 2 vez(es) na semana': '1 ou 2 por semana',
    '1 ou 2 vez(es) por mês': '1 ou 2 por mês',
    '3 a 6 vezes na semana': '3 a 6 por semana',
    '7 vezes por semana': 'Todos os dias',
    '1 ou 2 vez(es) a cada três meses': '1 ou 2 a cada 3 meses',
    'Menos que qualquer uma alternativa': 'Menos que qualquer uma',
}

dados_filtrados['Frequencia uso'] = dados_filtrados['Frequencia uso'].map(mapemamento)

mapemamento = {
    'Uso diário (no trabalho, escola ou atividades cotidianas)': 'Uso diário',
    'Lazer (encontros casuais, passeios, atividades de tempo livre)': 'Lazer',
    'Eventos sociais (festas e celebrações)': 'Eventos sociais',
    'Ocasiões formais (como casamentos, formaturas ou eventos corporativos)': 'Ocasiões formais',
}

dados_filtrados['Utilização'] = dados_filtrados['Utilização'].map(mapemamento)

# Calcular número de respondentes e idade média
idade_media = round(dados_filtrados['Idade_Num'].mean())
num_respondentes = len(dados_filtrados)
local = dados_filtrados['Região'].value_counts().index[0] if not dados_filtrados['Região'].empty else 'Sem dados'
frequencia = dados_filtrados['Frequência'].value_counts().index[0] if not dados_filtrados['Frequência'].empty else 'Sem dados'

cols = st.columns([1, 2, 2])
with cols[0]:
    st.markdown(
        f"""
        <div style='background-color: #586e75; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>
            <h3>Número de Respondentes: {num_respondentes}</h3>
        </div>
        <div style='background-color: #586e75; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>
            <h3>Idade Média: {idade_media}</h3>
        </div>
        <div style='background-color: #586e75; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>
            <h3>Região: {local}</h3>
        </div>
        <div style='background-color: #586e75; padding: 10px; border-radius: 10px;'>
            <h3>Frequência de Compra: {frequencia}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
with cols[1]:
    age_counts = dados_filtrados['Idade'].value_counts().reindex(age_mapping.keys(), fill_value=0)
    fig = create_bar_chart(age_counts, "Faixa Etária", "Faixa Etária", "Número de Respondentes", 45)
    if fig:
        st.plotly_chart(fig)
    
with cols[2]:
    lugar_counts = dados_filtrados['Lugar'].value_counts()
    fig = create_bar_chart(lugar_counts, "Meio de aquisição", "Lugar", "Número de Respondentes", 45)
    if fig:
        st.plotly_chart(fig)

cols2 = st.columns(3)
with cols2[0]:
    regiao_counts = dados_filtrados['Região'].value_counts()
    fig = create_bar_chart(regiao_counts, "Regiões", "Região", "Número de Respondentes", 45)
    if fig:
        st.plotly_chart(fig)

with cols2[1]:
    frequencia_counts = dados_filtrados['Frequência'].value_counts()
    fig = create_bar_chart(frequencia_counts, "Frequência de Compra", "Frequência", "Número de Respondentes", 45)
    if fig:
        st.plotly_chart(fig)

with cols2[2]:
    dados_filtrados_copy = dados_filtrados.copy()
    dados_filtrados_copy['Marcas'] = dados_filtrados_copy['Marcas'].str.split(',')
    dados_exploded = dados_filtrados_copy.explode('Marcas')
    marca_counts = dados_exploded['Marcas'].value_counts()
    fig = create_bar_chart(marca_counts, "Marcas Conhecidas", "Marcas", "Número de Ocorrências", 45)
    if fig:
        st.plotly_chart(fig)

cols3 = st.columns(3)
with cols3[0]:
    dados_filtrados_copy = dados_filtrados.copy()
    dados_filtrados_copy['Características'] = dados_filtrados_copy['Características'].str.split(',')
    dados_exploded = dados_filtrados_copy.explode('Características')
    caracter_counts = dados_exploded['Características'].value_counts()
    fig = create_bar_chart(caracter_counts, "Associações com Paula Torres", "Características", "Número de Ocorrências", 45)
    if fig:
        st.plotly_chart(fig)

with cols3[1]:
    dados_filtrados_copy = dados_filtrados.copy()
    dados_filtrados_copy['Falta na marca'] = dados_filtrados_copy['Falta na marca'].str.split(',')
    dados_exploded = dados_filtrados_copy.explode('Falta na marca')
    # Mapeamento reduzido de palavras
    mapping = {
        'Melhor relação custo-benefício': 'Custo-benefício',
        'Qualidade do produto': 'Qualidade',
        'Promoções e descontos mais frequentes': 'Promoções',
        'Mais opções de estilo e design': 'Estilo/design',
        'Não tem uma loja física perto': 'Sem loja física',
        'Outros': 'Outros',
        'Presença mais forte nas redes sociais': 'Redes sociais',
        'Estratégias de marketing mais atraente': 'Marketing',
        'Atendimento ao cliente superior': 'Atendimento',
        'Iniciativas de sustentabilidade mais atrativas': 'Sustentabilidade'
    }
    dados_exploded['Falta na marca'] = dados_exploded['Falta na marca'].str.strip().map(mapping)

    # Conta as ocorrências das palavras-chave
    caracter_counts = dados_exploded['Falta na marca'].value_counts()
    
    fig = create_bar_chart(caracter_counts, "Diferenciais das Outras Marcas com a Paula Torres", "Características", "Número de Ocorrências", 45)
    if fig:
        st.plotly_chart(fig)

with cols3[2]:
    dados_filtrados_copy = dados_filtrados.copy()
    dados_filtrados_copy['Diferencial'] = dados_filtrados_copy['Diferencial'].str.split(',')
    dados_exploded = dados_filtrados_copy.explode('Diferencial')
    mapemamento = {
    'Qualidade dos produtos': 'Qualidade',
    'Design': 'Design',
    'Conforto': 'Conforto',
    'Trabalho artesanal': 'Trabalho Artesanal',
    'Atualização de modelos': 'Atualização de modelos',
    'Inovação': 'Inovação',
    'Susentabilidade': 'Sustentabilidade',
    'Outros': 'Outros',
    }
    dados_exploded['Diferencial'] = dados_exploded['Diferencial'].map(mapemamento)

    diferencial_counts = dados_exploded['Diferencial'].value_counts()

    fig = create_bar_chart(diferencial_counts, " Diferenciais da Paula Torres", "Pontos diferencias", "Número de Ocorrências", 45)
    if fig:
        st.plotly_chart(fig)

cols4 = st.columns(3)
with cols4[0]:
    dados_filtrados_copy = dados_filtrados.copy()
    dados_filtrados_copy['Pontos melhora'] = dados_filtrados_copy['Pontos melhora'].str.split(',')
    dados_exploded = dados_filtrados_copy.explode('Pontos melhora')
    mapemamento = {
        'Preço': 'Preço',
        'Qualidade dos produtos': 'Qualidade',
        'Diversificação de modelos': 'Diversificação',
        'Conforto': 'Conforto',
        'Atualização de modelos': 'Atualização',
        'Exclusividade': 'Exclusividade',
        'Design': 'Design',
        'Inovação': 'Inovação',
        'Outros': 'Outros',
        'Trabalho artesanal': 'Trabalho Artesanal',
        'Sustentabilidade': 'Sustentabilidade',
    }
    dados_exploded['Pontos melhora'] = dados_exploded['Pontos melhora'].map(mapemamento)
    pontos_melhora_counts = dados_exploded['Pontos melhora'].value_counts()
    fig = create_bar_chart(pontos_melhora_counts, "Pontos de melhora da Paula Torres", "Pontos de melhora", "Número de Ocorrências", 45)
    if fig:
        st.plotly_chart(fig)

with cols4[1]:
    q53_counts = dados_filtrados['Q40'].value_counts()
    fig = create_bar_chart(q53_counts, "Valoriza uma linha que acompanha as tendências", "Resposta", "Número de Respondentes", 45)
    if fig:
        st.plotly_chart(fig)

with cols4[2]:
    q54_counts = dados_filtrados['Q41'].value_counts().sort_index()
    fig = create_bar_chart(q54_counts, "O quanto que a Paula Torres acompanha tendências", "5 - Acompanha muito, 1 - Não acompanha", "Número de Respondentes", 45)
    if fig:
        st.plotly_chart(fig)

cols5 = st.columns(3)
with cols5[0]:
    lancamentos_counts = dados_filtrados['Lançamentos'].value_counts().sort_index()
    fig = create_bar_chart(lancamentos_counts, "Importância de lançamentos frequentes", "Importância", "Número de Respondentes", 45)
    if fig:
        st.plotly_chart(fig)

with cols5[1]:
    dados_filtrados_copy = dados_filtrados.copy()
    dados_filtrados_copy['Procura'] = dados_filtrados_copy['Procura'].str.split(',')
    dados_exploded = dados_filtrados_copy.explode('Procura')
    mapemamento = {
        'Acessa o site da marca diretamente': 'Site',
        'Busca tendências de moda em redes sociais': 'Redes Sociais',
        'Visita lojas físicas para experimentar pessoalmente': 'Visita Loja Física',
        'Procura pelo produto específico na internet': 'Internet',
        'Outros': 'Outros',
        'Pede recomendações para conhecidos': 'Recomendação',
        'Assiste vídeos de reviews': 'Vídeos de Reviews',
    }
    dados_exploded['Procura'] = dados_exploded['Procura'].map(mapemamento)
    procura_counts = dados_exploded['Procura'].value_counts()
    fig = create_bar_chart(procura_counts, "Pesquisa de Novos Sapatos", "Local de procura", "Número de Ocorrências", 45)
    if fig:
        st.plotly_chart(fig)

with cols5[2]:
    q30_counts = dados_filtrados['Canal Influencia'].value_counts()
    fig = create_bar_chart(q30_counts, "Que canal mais influencia na compra de um sapato", "Influências", "Número de Respondentes", 45)
    if fig:
        st.plotly_chart(fig)

cols6 = st.columns(3)
with cols6[0]:
    relevant_columns = ['Q45_1', 'Q45_2', 'Q45_3', 'Q45_4', 'Q45_5']
    if all(col in dados_filtrados.columns for col in relevant_columns):
        data = dados_filtrados[relevant_columns]

    data.columns = ['Durabilidade', 'Design', 'Preço', 'Qualidade', 'Conforto']
    relevant_columns = data.columns

    # Calculate value counts for each column
    counts = {col: data[col].value_counts().sort_index() for col in relevant_columns}

    # Plotly bar chart
    fig = go.Figure()

    bar_width = 0.15
    colors = ['#2079F8', '#1AA884', '#EF6868', '#DC267F', '#5114C6']
    labels = [str(5-i) for i in range(5)]

    # Creating horizontal bars
    for i, (column, color) in enumerate(zip(relevant_columns, colors)):
        fig.add_trace(go.Bar(
            y=[x + i * bar_width for x in range(len(counts[column]))],
            x=counts[column],
            orientation='h',
            name=labels[i],
            marker=dict(color=color),
        ))

        # Update layout for dark theme
        fig.update_layout(
            title='Classificação dos Aspectos em Ordem de Importância',
            xaxis_title='Frequency',
            yaxis_title='Aspects',
            yaxis=dict(
                tickmode='array',
                tickvals=[x + bar_width for x in range(len(counts[relevant_columns[0]]))],
                ticktext=relevant_columns,
            ),
            plot_bgcolor='white',  # Ajuste para fundo branco
            paper_bgcolor='white',  # Ajuste para fundo branco
            font=dict(color='black'),  # Texto em preto para melhor contraste
            legend=dict(
                bgcolor='white',
                bordercolor='white',
                font=dict(color='black')
            )
        )

    # Display the plot in Streamlit
    st.plotly_chart(fig)
    
with cols6[1]:
    frequencia_uso_counts = dados_filtrados['Frequencia uso'].value_counts()
    fig = create_bar_chart(frequencia_uso_counts, "Frequência de Uso", "Frequência", "Número de Respondentes", 45)
    if fig:
        st.plotly_chart(fig)

with cols6[2]:
    preco_counts = dados_filtrados['Preço'].value_counts().sort_index()
    fig = create_bar_chart(preco_counts, "O quão justificável são os preços", "1 - Injusto, 5 - Justo", "Número de Respondentes", 45)
    if fig:
        st.plotly_chart(fig)

cols7 = st.columns(3)
with cols7[0]:
    utilizacao_counts = dados_filtrados['Utilização'].value_counts()
    fig = create_bar_chart(utilizacao_counts, "Ocasiões de Uso", "Ocasião", "Número de Respondentes", 45)
    if fig:
        st.plotly_chart(fig)
    
with cols7[1]:
    dados_filtrados_copy = data_all.copy()
    dados_filtrados_copy['Qualidades marcas'] = dados_filtrados_copy['Qualidades marcas'].str.split(',')
    dados_exploded = dados_filtrados_copy.explode('Qualidades marcas')
    
    mapping_qualidade = {
    'Informações sobre a qualidade do e o conforto do sapato': 'Qualidade/conforto',
    'Variedade de estilos e peças': 'Variedade',
    'Promoções/descontos': 'Promoções',
    'Avaliações e opiniões positivas de outros clientes': 'Opiniões positivas',
    'Recomendações de amigos/familiares': 'Recomendações',
    'Compromisso da marca com a sustentabilidade': 'Sustentabilidade',
    'Publicidade criativa e atraente': 'Publicidade',
    'Outros': 'Outros',
    'Parceria com influenciadores e celebridades': 'Influenciadores'
    }
    dados_exploded['Qualidades marcas'] = dados_exploded['Qualidades marcas'].map(mapping_qualidade)
    caracter_counts = dados_exploded['Qualidades marcas'].value_counts()
    fig = create_bar_chart(caracter_counts, "Motivos para Experimentar Marcas", "Características", "Número de Ocorrências", 45)
    if fig:
        st.plotly_chart(fig)
    
with cols7[2]:
    q_34_counts = dados_filtrados['Q34'].value_counts()
    fig = create_bar_chart(q_34_counts, "Como conheceram a marca", "Canal", "Número de Respondentes", 45)
    if fig:
        st.plotly_chart(fig)
    
cols8 = st.columns(3)
with cols8[0]:
    q_30_counts = dados_filtrados['Qualidade'].value_counts()
    fig = create_bar_chart(q_30_counts, "Quão satisfeito está com os produtos/serviços", "Canal", "Número de Respondentes", 45)
    if fig:
        st.plotly_chart(fig)
