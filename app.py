import streamlit as st
import pymysql
import pandas as pd
import base64
import os
import plotly.express as px  # <--- ESSA LINHA ESTAVA FALTANDO

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Caracterização Pokémon", 
    page_icon="◓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CARREGAR FONTE COOLVETICA ---
def carregar_fonte_local(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        return f"""
            <style>
            @font-face {{
                font-family: 'Coolvetica';
                src: url(data:font/otf;base64,{encoded}) format('opentype');
            }}
            </style>
        """
    return ""

css_fonte = carregar_fonte_local("coolvetica.otf")
st.markdown(css_fonte, unsafe_allow_html=True)

# --- CARREGAR IMAGEM DA POKEBOLA ---
def codificar_imagem_base64(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        return f"data:image/png;base64,{encoded}"
    return ""

img_pokeball_base64 = codificar_imagem_base64("pokeball.png")

# --- 3. CSS GLOBAL (INCLUINDO O TEMA DO CÓDIGO) ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

/* --- Novo Pokeball Marca D'água (Baseado em Imagem) --- */
.pokeball-bg-final {{ 
    position: absolute;
    right: -250px;
    top: 0px; 
    width: 600px;
    height: 600px;
    background-image: url('{img_pokeball_base64}');
    background-size: contain;
    background-repeat: no-repeat;
    opacity: 0.1;
    pointer-events: none;
    z-index: 0;
}}

:root {{ 
    --bg-color: #F8FAFC;
    --text-main: #1E293B;       
    --text-light: #64748B;      
    --card-bg: #FFFFFF;       
    --red-pk: #DC2626;            
    --cherry-pk: #CC0000;            
    --yellow-pk: #FFDE00;       
    --blue-pk: #2563EB;       
    --gold-pk: #B3A125;       
    --chumbo: #374151;
    
    /* 5 Cores da Faixa */
    --fs-1: #FF0000;
    --fs-2: #CC0000;
    --fs-3: #3B4CCA;
    --fs-4: #FFDE00;
    --fs-5: #B3A125;
}}

.stApp {{
    background-color: var(--bg-color);
    color: var(--text-main);
    font-family: 'Coolvetica', sans-serif !important;
}}

/* Ajuste de Topo */
.block-container {{
    padding-top: 2rem !important; 
    padding-left: 4rem !important; 
    padding-right: 4rem !important;
    max-width: 100% !important;
}}

/* Faixa Lateral Fixa */
.fixed-sidebar {{
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: 18px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
}}
.fs-1 {{ flex: 1; background-color: var(--fs-1); }}
.fs-2 {{ flex: 1; background-color: var(--fs-2); }}
.fs-3 {{ flex: 1; background-color: var(--fs-3); }}
.fs-4 {{ flex: 1; background-color: var(--fs-4); }}
.fs-5 {{ flex: 1; background-color: var(--fs-5); }}

/* Estilo das Abas */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px; 
    border-bottom: 1px solid #E2E8F0;
    margin-bottom: 40px;
    display: flex;
    width: 100%;
}}

.stTabs [data-baseweb="tab"] {{
    height: 60px;
    background-color: transparent;
    color: #94a3b8;
    font-weight: 600;
    border: none;
    font-family: 'Coolvetica', sans-serif !important;
    text-transform: uppercase;
    font-size: 1rem; 
    letter-spacing: 1px;
    flex: 1; 
    width: 100%;
    justify-content: center;
}}

.stTabs [aria-selected="true"] {{
    color: var(--cherry-pk) !important;
    box-shadow: 0px 3px 0px 0px var(--cherry-pk);
}}

h1, h2, h3 {{ 
    font-family: 'Coolvetica', sans-serif !important; 
    font-weight: 400 !important; /* Remove o negrito forçado do Streamlit */
    letter-spacing: 1px; /* Dá um respiro entre as letras */
    -webkit-text-stroke: 0px !important; /* Garante que não tenha borda extra */
    text-shadow: none !important; /* Remove sombras se houver */
}}


/* --- ESTILOS DA CAPA --- */
.titulo-capa {{
    font-family: 'Coolvetica', sans-serif !important;
    color: var(--cherry-pk) !important;
    font-size: 100rem;
    line-height: 1; 
    margin-bottom: 0px
    text-transform: uppercase;
    text-align: left;
}}
.subtitulo-capa {{
    font-family: 'Coolvetica', sans-serif !important;
    color: var(--chumbo-pk) !important;
    font-size: 3.5rem; 
    line-height: 1; 
    margin-top: -30px !important; 
    font-weight: 10 !important; 
    text-align: left;
}}

a {{ color: var(--blue-pk) !important; text-decoration: none; }}
.stDataFrame, code {{ font-family: Consolas, monospace !important; }}

/* --- COLORIZAÇÃO DE CÓDIGO (TEMA POKÉMON) --- */

/* Força o fundo do bloco de código para branco e texto preto */
.stCodeBlock, .stCodeBlock > div, .stCodeBlock code {{
    background-color: #ffffff !important;
    color: #000000 !important; /* Texto Base Preto */
}}

/* Keywords (SELECT, FROM, CREATE, WHERE) -> AZUL */
code[class*="language-"] .token.keyword {{
    color: #3B4CCA !important;
    font-weight: bold !important;
}}

/* Funções e Classes (COUNT, INT, VARCHAR) -> Cherry */
code[class*="language-"] .token.function, 
code[class*="language-"] .token.class-name, 
code[class*="language-"] .token.builtin {{
    color: #CC0000 !important;
    font-weight: bold !important;
}}

/* Strings (Texto entre aspas) -> Dourado */
code[class*="language-"] .token.string {{
    color: #B3A125 !important;
}}

/* Números -> Vermelho Escuro */
code[class*="language-"] .token.number {{
    color: #FF0000 !important;
}}

/* Operadores e Pontuação (=, >, ;) -> Azul */
code[class*="language-"] .token.operator,
code[class*="language-"] .token.punctuation {{
    color: #3B4CCA !important;
}}

/* Comentários -> Cinza */
code[class*="language-"] .token.comment {{
    color: #9ca3af !important;
}}

</style>
""", unsafe_allow_html=True)

# --- 4. HTML DA BARRA LATERAL ---
st.markdown("""
<div class="fixed-sidebar">
<div class="fs-1"></div>
<div class="fs-2"></div>
<div class="fs-3"></div>
<div class="fs-4"></div>
<div class="fs-5"></div>
</div>
""", unsafe_allow_html=True)

# --- 5. DADOS (FINAL MESMO - SEM LIMITES NA ELITE) ---
CONSULTAS_INFO = {
    "Catálogo Completo": {
        "subtitulo": "Uma lista geral unindo as principais informações: Nome, onde vive (Região) e qual seu elemento (Tipo).",
        "sql": "SELECT P.Nome, G.Regiao, T.Nome as Tipo FROM Pokemon P JOIN Geracao G ON P.idGeracao = G.Numero JOIN Pertence PT ON P.Numero = PT.Numero JOIN Tipo T ON PT.Nome = T.Nome"
    },
    "Ranking de Força por Tipo": {
        "subtitulo": "Calculamos a média de ataque de cada elemento. Qual tipo de Pokémon costuma ser fisicamente mais forte?",
        "sql": "SELECT T.Nome as Tipo, ROUND(AVG(P.Ataque),2) as Media_Ataque FROM Tipo T JOIN Pertence PT ON T.Nome = PT.Nome JOIN Pokemon P ON PT.Numero = P.Numero GROUP BY T.Nome ORDER BY Media_Ataque DESC"
    },
    "A Elite (Acima da Média)": {
        "subtitulo": "Filtramos apenas os Pokémons que possuem Ataque superior à média global de todos os registros.",
        # TIREI O 'LIMIT 50' DAQUI:
        "sql": "SELECT Nome, Ataque FROM Pokemon WHERE Ataque > (SELECT AVG(Ataque) FROM Pokemon) ORDER BY Ataque DESC"
    },
    "Exemplos de Cada Elemento": {
        "subtitulo": "Uma listagem para conferir todos os Tipos existentes no banco e um exemplo de Pokémon para cada um.",
        "sql": "SELECT T.Nome as Tipo, P.Nome as Exemplo FROM Tipo T LEFT JOIN Pertence PT ON T.Nome = PT.Nome LEFT JOIN Pokemon P ON PT.Numero = P.Numero GROUP BY T.Nome"
    },
    "Os Tipos Mais Resistentes": {
        "subtitulo": "Uma análise de Defesa: quais elementos têm, em média, a maior capacidade de proteção?",
        "sql": "SELECT T.Nome, ROUND(AVG(P.Defesa),2) as Media_Defesa FROM Tipo T JOIN Pertence PT ON T.Nome = PT.Nome JOIN Pokemon P ON PT.Numero = P.Numero GROUP BY T.Nome HAVING AVG(P.Defesa) > (SELECT AVG(Defesa) FROM Pokemon) ORDER BY Media_Defesa DESC"
    },
    "O Campeão de Cada Região": {
        "subtitulo": "Identificamos o Pokémon mais forte (maior ataque) de cada uma das regiões geográficas do jogo.",
        "sql": "SELECT P.Nome, P.Ataque, G.Regiao FROM Pokemon P JOIN Geracao G ON P.idGeracao = G.Numero WHERE P.Ataque = (SELECT MAX(P2.Ataque) FROM Pokemon P2 WHERE P2.idGeracao = P.idGeracao) ORDER BY G.Regiao"
    },
    "População por Região": {
        "subtitulo": "Quantos Pokémons foram descobertos em cada região? Um censo da distribuição demográfica.",
        "sql": "SELECT G.Regiao, COUNT(*) as Total FROM Pokemon P JOIN Geracao G ON P.idGeracao = G.Numero GROUP BY G.Regiao"
    },
    "Top 10: Melhores Defesas": {
        "subtitulo": "O ranking definitivo dos 10 Pokémons com os maiores atributos de defesa individual.",
        "sql": "SELECT Nome, Defesa FROM Pokemon ORDER BY Defesa DESC LIMIT 10"
    }
}

def get_data(query):
    try:
        conn = pymysql.connect(host="localhost", user="root", password="", database="trabalho_pokemon", cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return pd.DataFrame(data) if data else pd.DataFrame()
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")
        return pd.DataFrame()

# --- 6. LAYOUT ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "INÍCIO", 
    "CONSULTAS", 
    "MODELO CONCEITUAL", 
    "MODELO RELACIONAL", 
    "MODELO FÍSICO"
])

# --- ABA 1: INÍCIO ---
with tab1:
    st.markdown("""
    <div class="pokeball-bg-final"></div> 
    """, unsafe_allow_html=True)
    
    # Título
    st.markdown("""
    <div style="position: relative; z-index: 1; margin-top: 40px;">
    <h1 class="titulo-capa">CARACTERIZAÇÃO DE POKÉMON</h1>
    <h2 class="subtitulo-capa">Introduzidos até a oitava geração</h2>
    </div>
    """, unsafe_allow_html=True)

    # ESPAÇADOR GRANDE PARA EMPURRAR CONTEÚDO PARA BAIXO
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 2], gap="small") 
    
    with c1:
        st.markdown("""
        <div style="padding: 0 20px;">
            <h2 style="color: #B3A125; font-family: 'Coolvetica'; font-size: 1.2rem; margin-bottom: 15px;">INTEGRANTES</h2>
            <ul style="list-style: none; padding: 0; font-family: 'Coolvetica'; font-size: 0.9rem; color: #475569; line-height: 1.5;">
                <li style="display: flex; align-items: center;"><span style="color: #FFDE00; margin-right: 8px;">|</span> Davi Alves</li>
                <li style="display: flex; align-items: center;"><span style="color: #FFDE00; margin-right: 8px;">|</span> Davi Brito</li>
                <li style="display: flex; align-items: center;"><span style="color: #FFDE00; margin-right: 8px;">|</span> Isabela Veiga</li>
                <li style="display: flex; align-items: center;"><span style="color: #FFDE00; margin-right: 8px;">|</span> Marcos Antônio de Lima</li>
                <li style="display: flex; align-items: center;"><span style="color: #FFDE00; margin-right: 8px;">|</span> Pedro Chaves</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown("""
        <div style="padding: 0 20px;">
            <h2 style="color: #B3A125; font-family: 'Coolvetica'; font-size: 1.2rem; margin-bottom: 15px;">REFERÊNCIAS</h2>
            <ul style="list-style: none; padding: 0; font-family: 'Coolvetica'; font-size: 0.9rem; color: #475569; line-height: 1.5;">
                <li style="display: flex; align-items: center;">
                    <span style="color: #FFDE00; margin-right: 8px;">|</span> 
                    <span>Dataset Primário: <a href="https://www.kaggle.com/datasets/maca11/all-pokemon-dataset" target="_blank">Kaggle - All Pokemon Dataset</a></span>
                </li>
                <li style="display: flex; align-items: center;">
                    <span style="color: #FFDE00; margin-right: 8px;">|</span> 
                    <span>Classificação Regional: <a href="https://m.bulbapedia.bulbagarden.net/wiki/Region" target="_blank">Bulbapedia - Region Data</a></span>
                </li>
                </ul>
        </div>
        """, unsafe_allow_html=True)


# --- ABA 2: CONSULTAS ---
with tab2:
    col_nav, col_content = st.columns([1, 3])
    with col_nav:
        st.markdown("##### CONSULTAS")
        escolha_menu = st.radio("Menu", list(CONSULTAS_INFO.keys()), label_visibility="collapsed")
    with col_content:
        dados = CONSULTAS_INFO[escolha_menu]
        sql_atual = dados["sql"]
        subtitulo = dados["subtitulo"]

        # Título Principal (Já estava em Cherry)
        st.markdown(f"<h1 style='font-size: 2.5rem; color: #CC0000 !important; border: none; margin-bottom: 10px;'>{escolha_menu.upper()}</h1>", unsafe_allow_html=True)
        
        # --- MUDANÇA AQUI: Subtítulo com "OBJETIVO" em Azul ---
        # Usamos HTML para colorir apenas a palavra "OBJETIVO:" com o azul da paleta (#3B4CCA)
        st.markdown(f"<p style='font-size: 1.1rem;'><span style='color: #3B4CCA; font-weight: bold;'>OBJETIVO:</span> {subtitulo}</p>", unsafe_allow_html=True)
        df = get_data(sql_atual)
        
        if not df.empty:
            t1, t2 = st.tabs(["GRÁFICOS", "TABELA DE DADOS"])
            with t2:
                st.dataframe(df, use_container_width=True)
                st.markdown("###### CÓDIGO SQL EXECUTADO:")
                st.code(sql_atual, language="sql")
            
            # --- LÓGICA DE GRÁFICOS COM PLOTLY (CORRIGIDA) ---
            # --- LÓGICA DE GRÁFICOS COM PLOTLY (ATUALIZADA PARA TOP 10 COLORIDO) ---
            # --- LÓGICA DE GRÁFICOS COM PLOTLY (PADRÃO: BARRAS COLORIDAS + TEXTO DENTRO) ---
            # --- LÓGICA DE GRÁFICOS COM PLOTLY (ATUALIZADA: CATÁLOGO COM TREEMAP) ---
            # --- LÓGICA DE GRÁFICOS COM PLOTLY (ATUALIZADA: CATÁLOGO COM TREEMAP MELHORADO) ---
            # --- LÓGICA DE GRÁFICOS COM PLOTLY (FINAL: TREEMAP AJUSTADO) ---
            # --- LÓGICA DE GRÁFICOS COM PLOTLY (FINAL: TREEMAP SEM AMARELO FORTE) ---
            # --- LÓGICA DE GRÁFICOS COM PLOTLY (FINAL: PALETA EXTENDIDA SEM ROXO) ---
            with t1:
                # Paleta Padrão para gráficos gerais
                CORES_POKEMON = ['#CC0000', '#3B4CCA', '#B3A125', '#FFDE00', '#1E293B']
                fig = None
                
                # 1. CASO ESPECIAL: CATÁLOGO (Treemap)
                if "Catálogo" in escolha_menu:
                    # NOVA PALETA DO TREEMAP (Expandida para não repetir)
                    # Removemos o Roxo e adicionamos Laranja e Verde
                    CORES_TREEMAP = [
                        '#CC0000', # Cherry (Vermelho)
                        '#1E293B', # Chumbo (Escuro)
                        '#B3A125', # Gold (Mostarda)
                        '#3B4CCA', # Azul Royal
                        '#D97706', # LARANJA (Novo! Ótimo contraste)
                        '#15803D', # VERDE (Novo! Para variar)
                        '#0284C7'  # Azul Claro (Para diferenciar Galar/Kalos)
                    ]
                    
                    fig = px.treemap(
                        df, 
                        path=[df.columns[1], df.columns[2]], # Região > Tipo
                        color=df.columns[1], 
                        color_discrete_sequence=CORES_TREEMAP
                    )
                    fig.update_traces(
                        root_color="lightgrey",
                        # Mantém o texto clarinho (#EEEEEE) para leitura em fundo escuro
                        textfont=dict(family="Coolvetica", size=20, color='#EEEEEE'),
                        textinfo="label+percent parent"
                    )
                    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

                # 2. Censo/Contagem (Donut Chart)
                elif "População" in escolha_menu or "Censo" in escolha_menu or "Total" in escolha_menu:
                    col_nome = df.columns[0]
                    col_valor = df.columns[1]
                    fig = px.pie(
                        df, names=col_nome, values=col_valor, 
                        hole=0.5, 
                        color_discrete_sequence=CORES_POKEMON
                    )
                    fig.update_traces(textinfo='value+percent')

                # 3. TODOS os outros (Barras Coloridas + Texto Dentro)
                else:
                    try:
                        col_x = df.columns[0] 
                        col_y = df.columns[1] 
                        
                        fig = px.bar(
                            df, x=col_x, y=col_y, 
                            text=col_y,
                            color=col_x, 
                            color_discrete_sequence=CORES_POKEMON
                        )
                        
                        fig.update_traces(
                            texttemplate='%{text:.2s}', 
                            textposition='inside', 
                            textfont_color='#FFFFFF'
                        )
                    except:
                        st.info("Visualização gráfica não disponível para estes dados.")

                # --- ESTILIZAÇÃO GERAL ---
                if fig:
                    if "Catálogo" not in escolha_menu:
                        fig.update_layout(
                            title_text='', title=None,
                            xaxis_title="", yaxis_title="",
                            font_family="Coolvetica",
                            font_color="#1E293B",
                            
                            legend=dict(
                                font=dict(family="Coolvetica", size=18, color="#1E293B"),
                                orientation="v",
                            ),
                            plot_bgcolor="rgba(0,0,0,0)",
                            paper_bgcolor="rgba(0,0,0,0)",
                            margin=dict(l=20, r=20, t=20, b=20),
                            height=450
                        )
                        fig.update_coloraxes(showscale=False)
                        
                        if "População" not in escolha_menu and "Censo" not in escolha_menu:
                            fig.update_layout(showlegend=False)
                            
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhum registro localizado ou erro na consulta.")

# --- ABAS 3, 4, 5 ---
with tab3:
    st.markdown("### MODELO CONCEITUAL")
    if os.path.exists("modelo_conceitual.jpg"):
        st.markdown('<div class="tech-img">', unsafe_allow_html=True)
        st.image("modelo_conceitual.jpg", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Imagem 'modelo_conceitual.jpg' não encontrada no diretório.")

with tab4:
    st.markdown("### MODELO LÓGICO")
    if os.path.exists("modelo_logico.jpg"):
        st.markdown('<div class="tech-img">', unsafe_allow_html=True)
        st.image("modelo_logico.jpg", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Imagem 'modelo_logico.jpg' não encontrada no diretório.")

with tab5:
    st.markdown("### MODELO FÍSICO")
    codigo_sql = """
CREATE TABLE Geracao (
    Regiao VARCHAR(255),
    Numero INT PRIMARY KEY
);

CREATE TABLE Pokemon (
    Numero INT PRIMARY KEY,
    Nome VARCHAR(255),
    Defesa INT,
    Ataque INT,
    idGeracao INT,
    FOREIGN KEY(idGeracao) REFERENCES Geracao (Numero)
);

CREATE TABLE Tipo (
    Imunidade TINYINT,
    Nome VARCHAR(255) PRIMARY KEY
);

CREATE TABLE Habilidade (
    Nome VARCHAR(255) PRIMARY KEY,
    Descricao TEXT
);

CREATE TABLE Possui (
    Numero INT,
    Nome VARCHAR(255),
    PRIMARY KEY (Numero, Nome),
    FOREIGN KEY(Numero) REFERENCES Pokemon (Numero),
    FOREIGN KEY(Nome) REFERENCES Habilidade (Nome)
);

CREATE TABLE Pertence (
    Nome VARCHAR(255),
    Numero INT,
    PRIMARY KEY (Nome, Numero),
    FOREIGN KEY(Nome) REFERENCES Tipo (Nome),
    FOREIGN KEY(Numero) REFERENCES Pokemon (Numero)
);

CREATE TABLE Efetividade (
    Multiplicador FLOAT,
    Nome VARCHAR(255) PRIMARY KEY,
    FOREIGN KEY(Nome) REFERENCES Tipo (Nome)
);
    """
    st.code(codigo_sql, language="sql")