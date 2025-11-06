import streamlit as st
import pandas as pd
import sqlite3
import altair as alt

# --- Configuração da Página ---
# Define o título da aba do navegador e o layout (wide = tela cheia)
st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

# --- REQUISITO DE ESTILO: Cor Azul Claro nos Filtros ---
# Injeta código CSS para estilizar os filtros multiselect
st.markdown("""
<style>
/* Cor azul claro para as "pills" (opções selecionadas) do multiselect */
[data-testid="stMultiSelect"] [data-baseweb="tag"] {
    background-color: #ADD8E6 !important; /* lightblue */
    color: #000000 !important; /* texto preto para contraste */
    border-radius: 0.25rem; /* cantos arredondados */
}
/* Cor do "x" de fechar a pill */
[data-testid="stMultiSelect"] [data-baseweb="tag"] span[role="presentation"] {
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)
# --- Fim do CSS ---

# --- Constantes de Configuração ---
# Define o caminho para o banco de dados e o nome da tabela
DB_FILE = "dados/teste.db"
TABLE_NAME = "mortes"

# Define os nomes das colunas que serão usadas
COL_ANO_MOR = 'ano_mor'
COL_CAUSA = 'causa'
COL_CLASS = 'classificacao'
COL_IDADE = 'idade'
COL_PATENTE = 'patente'
COL_SERVICO = 'servico'
COL_TIPO_LOCAL = 'tipo_local'
COL_NATU = 'natu'

# --- Carregamento de Dados ---
# @st.cache_data armazena o resultado da função em cache para performance
@st.cache_data(ttl=600)
def load_data_from_db():
    """
    Carrega os dados do banco SQLite e faz uma limpeza leve.
    Assume que o tratamento principal (RF02) foi feito no R.
    """
    try:
        
        conn = sqlite3.connect(DB_FILE)
        query = f"SELECT * FROM {TABLE_NAME}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Garante que colunas numéricas são do tipo numérico
        df[COL_ANO_MOR] = pd.to_numeric(df[COL_ANO_MOR], errors='coerce')
        df[COL_IDADE] = pd.to_numeric(df[COL_IDADE], errors='coerce')
        
        # Remove linhas onde dados essenciais (ano, idade) são nulos
        df = df.dropna(subset=[COL_ANO_MOR, COL_IDADE])
        
        # Preenche nulos (NaN) em colunas de texto com "Desconhecido"
      
        cols_de_texto = [COL_CAUSA, COL_CLASS, COL_PATENTE, COL_SERVICO, COL_TIPO_LOCAL, COL_NATU]
        for col in cols_de_texto:
            if col in df.columns: 
                df[col] = df[col].fillna("Desconhecido") 
            
        return df
        
    except Exception as e:
        # Mostra um erro amigável se o banco de dados não for encontrado
        st.error(f"ERRO: Não foi possível ler a tabela '{TABLE_NAME}' do '{DB_FILE}'.")
        st.exception(e)
        return None

# Executa a função de carregamento
df_original = load_data_from_db()

# Para a execução se os dados não foram carregados
if df_original is None:
    st.error("Não foi possível carregar os dados. A aplicação será interrompida.")
    st.stop()

# --- Barra Lateral de Filtros (Sidebar) ---
st.sidebar.header("Filtros")

# --- Filtro 1: Ano ---
anos_disponiveis = sorted(df_original[COL_ANO_MOR].unique().astype(int))
# Usa st.session_state para "lembrar" as seleções
if 'anos_selecionados' not in st.session_state:
    st.session_state.anos_selecionados = anos_disponiveis # Começa com todos marcados

# Cria o widget multiselect (dropdown com checkbox)
st.sidebar.multiselect(
    "Selecione o(s) Ano(s):",
    options=anos_disponiveis,
    key='anos_selecionados' # Liga o widget ao session_state
)
# Botões para marcar/desmarcar todos
col_ano1, col_ano2 = st.sidebar.columns(2)
if col_ano1.button("Marcar Todos", use_container_width=True, key='btn_ano_all'):
    st.session_state.anos_selecionados = anos_disponiveis
    st.rerun() # Recarrega a página para aplicar a mudança
if col_ano2.button("Desmarcar Todos", use_container_width=True, key='btn_ano_none'):
    st.session_state.anos_selecionados = []
    st.rerun()
st.sidebar.divider() # Linha divisória

# --- Filtro 2: Classificação ---
classes_disponiveis = df_original[COL_CLASS].unique()
if 'classes_selecionadas' not in st.session_state:
    st.session_state.classes_selecionadas = classes_disponiveis

st.sidebar.multiselect(
    "Selecione a Classificação:",
    options=classes_disponiveis,
    key='classes_selecionadas'
)
col_class1, col_class2 = st.sidebar.columns(2)
if col_class1.button("Marcar Todas", use_container_width=True, key='btn_class_all'):
    st.session_state.classes_selecionadas = classes_disponiveis
    st.rerun()
if col_class2.button("Desmarcar Todas", use_container_width=True, key='btn_class_none'):
    st.session_state.classes_selecionadas = []
    st.rerun()
st.sidebar.divider()

# --- Filtro 3: Causa ---
causas_disponiveis = df_original[COL_CAUSA].unique()
if 'causas_selecionadas' not in st.session_state:
    st.session_state.causas_selecionadas = causas_disponiveis
    
st.sidebar.multiselect(
    "Selecione a Causa:",
    options=causas_disponiveis,
    key='causas_selecionadas'
)
col_causa1, col_causa2 = st.sidebar.columns(2)
if col_causa1.button("Marcar Todas", use_container_width=True, key='btn_causa_all'):
    st.session_state.causas_selecionadas = causas_disponiveis
    st.rerun()
if col_causa2.button("Desmarcar Todas", use_container_width=True, key='btn_causa_none'):
    st.session_state.causas_selecionadas = []
    st.rerun()
st.sidebar.divider()

# --- Filtro 4: Serviço ---
servicos_disponiveis = df_original[COL_SERVICO].unique()
if 'servicos_selecionados' not in st.session_state:
    st.session_state.servicos_selecionados = servicos_disponiveis

st.sidebar.multiselect(
    "Selecione o Tipo de Serviço:",
    options=servicos_disponiveis,
    key='servicos_selecionados'
)
col_serv1, col_serv2 = st.sidebar.columns(2)
if col_serv1.button("Marcar Todos", use_container_width=True, key='btn_serv_all'):
    st.session_state.servicos_selecionados = servicos_disponiveis
    st.rerun()
if col_serv2.button("Desmarcar Todos", use_container_width=True, key='btn_serv_none'):
    st.session_state.servicos_selecionados = []
    st.rerun()
# --- Fim dos Filtros ---

# --- Aplicação dos Filtros ---
# Filtra o DataFrame original com base nas seleções guardadas no session_state
df_filtrado = df_original[
    (df_original[COL_ANO_MOR].isin(st.session_state.anos_selecionados)) &
    (df_original[COL_CLASS].isin(st.session_state.classes_selecionadas)) &
    (df_original[COL_CAUSA].isin(st.session_state.causas_selecionadas)) &
    (df_original[COL_SERVICO].isin(st.session_state.servicos_selecionados))
]

# --- Início do Layout Principal ---
st.title("Análise de Fatalidades de Bombeiros")

# --- KPIs  ---
st.header("Visão Geral (Filtrada)")


if not df_filtrado.empty:
    total_fatalidades = len(df_filtrado)
    media_idade = int(df_filtrado[COL_IDADE].mean())
    patente_comun = df_filtrado[COL_PATENTE].mode()[0]

  
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Fatalidades ", f"{total_fatalidades}")
    col2.metric("Idade Média ", f"{media_idade} anos")
    col3.metric("Patente Mais Comun", patente_comun)
else:
    
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop() 

st.divider()

# --- Secção de Gráficos ---
st.header("Análises Visuais")

col1, col2 = st.columns(2)

with col1:
    # Gráfico 1: HISTOGRAMA DE IDADE
    st.subheader("Distribuição de Idade das Fatalidades")
    hist_idade = alt.Chart(df_filtrado).mark_bar().encode(
        x=alt.X(f"{COL_IDADE}:Q", bin=alt.Bin(maxbins=20), title="Faixa Etária"),
        y=alt.Y('count()', title="Número de Fatalidades"),
        tooltip=[alt.Tooltip(f"{COL_IDADE}:Q", bin=True), 'count()']
    ) 
    st.altair_chart(hist_idade, use_container_width=True)
    
    # Gráfico 2: Top 10 Patentes
    st.subheader("Top 10 Patentes com Mais Fatalidades")
    chart_patente_data = df_filtrado.groupby(COL_PATENTE).size().reset_index(name='contagem') \
        .sort_values(by='contagem', ascending=False).head(10)

    chart_patente = alt.Chart(chart_patente_data).mark_bar().encode(
        x=alt.X('contagem', title='Número de Fatalidades'),
        y=alt.Y(COL_PATENTE, title='Patente', sort='-x'),
        tooltip=[COL_PATENTE, 'contagem']
    )
    st.altair_chart(chart_patente, use_container_width=True)

with col2:
    # Gráfico 3: Top 10 Causas
    st.subheader("Principais Causas de Fatalidade")
    top_10_causas = df_filtrado[COL_CAUSA].value_counts().head(10).index.tolist()
    df_top_causas = df_filtrado[df_filtrado[COL_CAUSA].isin(top_10_causas)]
    
    chart_causa = alt.Chart(df_top_causas).mark_bar().encode(
        x=alt.X('count()', title='Número de Fatalidades'),
        y=alt.Y(COL_CAUSA, title='Causa', sort='-x'),
        tooltip=[COL_CAUSA, 'count()'],
        color=COL_CAUSA
    ) 
    st.altair_chart(chart_causa, use_container_width=True)
    
    # Gráfico 4: Tipo de Local (Pizza)
    st.subheader("Fatalidades por Tipo de Local")
    chart_local = alt.Chart(df_filtrado).mark_arc(outerRadius=120).encode(
        theta=alt.Theta("count()", stack=True),
        color=alt.Color(COL_TIPO_LOCAL, title="Tipo de Local"),
        tooltip=[COL_TIPO_LOCAL, 'count()']
    ) 
    st.altair_chart(chart_local, use_container_width=True)

# Gráfico 5: Evolução por Ano (Linha)
st.subheader("Evolução das Fatalidades por Ano")
df_ano = df_filtrado[df_filtrado[COL_ANO_MOR].isin(st.session_state.anos_selecionados)]
chart_ano_data = df_ano.groupby(COL_ANO_MOR).size().reset_index(name='contagem')

line_chart = alt.Chart(chart_ano_data).mark_line(point=True).encode(
    x=alt.X(COL_ANO_MOR, title='Ano', axis=alt.Axis(format='d')), # 'd' = formato inteiro
    y=alt.Y('contagem', title='Número de Fatalidades'),
    tooltip=[COL_ANO_MOR, 'contagem']
) 

st.altair_chart(line_chart, use_container_width=True)

st.divider() # Linha divisória

# --- Tabela de Dados ---
st.header("Explorar Dados Completos (Filtrados)")
st.dataframe(df_filtrado)