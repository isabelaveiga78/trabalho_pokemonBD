import streamlit as st
import pymysql
import pandas as pd
import base64
import os
import plotly.express as px
import ssl

st.set_page_config(
    page_title="Caracterização Pokémon", 
    page_icon="◓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

def codificar_imagem_base64(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        return f"data:image/png;base64,{encoded}"
    return ""

img_pokeball_base64 = codificar_imagem_base64("pokeball.png")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

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

.block-container {{
    padding-top: 2rem !important; 
    padding-left: 4rem !important; 
    padding-right: 4rem !important;
    max-width: 100% !important;
}}

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
    font-weight: 400 !important;
    letter-spacing: 1px;
    -webkit-text-stroke: 0px !important;
    text-shadow: none !important;
}}

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

.stCodeBlock, .stCodeBlock > div, .stCodeBlock code {{
    background-color: #ffffff !important;
    color: #000000 !important;
}}

code[class*="language-"] .token.keyword {{
    color: #3B4CCA !important;
    font-weight: bold !important;
}}

code[class*="language-"] .token.function, 
code[class*="language-"] .token.class-name, 
code[class*="language-"] .token.builtin {{
    color: #CC0000 !important;
    font-weight: bold !important;
}}

code[class*="language-"] .token.string {{
    color: #B3A125 !important;
}}

code[class*="language-"] .token.number {{
    color: #FF0000 !important;
}}

code[class*="language-"] .token.operator,
code[class*="language-"] .token.punctuation {{
    color: #3B4CCA !important;
}}

code[class*="language-"] .token.comment {{
    color: #9ca3af !important;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="fixed-sidebar">
<div class="fs-1"></div>
<div class="fs-2"></div>
<div class="fs-3"></div>
<div class="fs-4"></div>
<div class="fs-5"></div>
</div>
""", unsafe_allow_html=True)

CONSULTAS_INFO = {
    "Catálogo Completo": {
        "subtitulo": "Uma lista geral unindo as principais informações: Nome, onde vive (Região) e qual seu elemento (Tipo).",
        "sql": "SELECT P.Nome, G.Regiao, T.Nome_pt as Tipo FROM Pokemon P JOIN Geracao G ON P.idGeracao = G.Numero JOIN Pertence PT ON P.Nome = PT.Pokemon JOIN Tipo T ON PT.Tipo = T.Nome"
    },
    "Ranking de Força por Tipo": {
        "subtitulo": "Calculamos a média de ataque de cada elemento. Qual tipo de Pokémon costuma ser fisicamente mais forte?",
        "sql": "SELECT T.Nome_pt as Tipo, ROUND(AVG(P.Ataque),2) as Media_Ataque FROM Tipo T JOIN Pertence PT ON T.Nome = PT.Tipo JOIN Pokemon P ON PT.Pokemon = P.Nome GROUP BY T.Nome_pt ORDER BY Media_Ataque DESC"
    },
    "A Elite (Acima da Média)": {
        "subtitulo": "Filtramos apenas os Pokémons que possuem Ataque superior à média global de todos os registros.",
        "sql": "SELECT Nome, Ataque FROM Pokemon WHERE Ataque > (SELECT AVG(Ataque) FROM Pokemon) ORDER BY Ataque DESC"
    },
    "Exemplos de Cada Combinação de Elemento": {
        "subtitulo": "Uma listagem para conferir todas as combinações de Tipos existentes e um exemplo de Pokémon para cada um.",
        "sql": "SELECT T1.Nome_pt as 'Tipo 1', T2.Nome_pt as 'Tipo 2', MAX(PT1.Nome) as Exemplo FROM (Tipo T1 JOIN Tipo T2 ON T1.Nome > T2.Nome) LEFT JOIN Pertence PT1 ON T1.Nome = PT1.Tipo LEFT JOIN Pertence PT2 ON T2.Nome = PT2.Tipo and PT1.Pokemon = PT2.Pokemon GROUP BY T1.Nome_pt, T2.Nome_pt"
    },
    "Os Tipos Mais Resistentes": {
        "subtitulo": "Uma análise de Defesa: quais elementos têm, em média, a maior capacidade de proteção?",
        "sql": "SELECT T.Nome_pt, ROUND(AVG(P.Defesa),2) as Media_Defesa FROM Tipo T JOIN Pertence PT ON T.Nome = PT.Tipo JOIN Pokemon P ON PT.Pokemon = P.Nome GROUP BY T.Nome HAVING AVG(P.Defesa) > (SELECT AVG(Defesa) FROM Pokemon) ORDER BY Media_Defesa DESC"
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
        # --- CONFIGURAÇÃO DE SSL ---
        # Isso cria um contexto que aceita a criptografia mas não exige certificado local
        # É o truque para funcionar na nuvem sem dor de cabeça
        conn = pymysql.connect(
            host=st.secrets["db_host"],
            user=st.secrets["db_user"],
            password=st.secrets["db_password"],
            database=st.secrets["db_name"],
            port=4000,
            cursorclass=pymysql.cursors.DictCursor,
            ssl={
                "check_hostname": False,
                "verify_mode": ssl.CERT_NONE
            }
        )
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return pd.DataFrame(data) if data else pd.DataFrame()
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")
        return pd.DataFrame()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "INÍCIO", 
    "CONSULTAS", 
    "MODELO CONCEITUAL", 
    "MODELO RELACIONAL", 
    "MODELO FÍSICO"
])

with tab1:
    st.markdown("""
    <div class="pokeball-bg-final"></div> 
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="position: relative; z-index: 1; margin-top: 40px;">
    <h1 class="titulo-capa">CARACTERIZAÇÃO DE POKÉMON</h1>
    <h2 class="subtitulo-capa">Introduzidos até a oitava geração</h2>
    </div>
    """, unsafe_allow_html=True)

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

with tab2:
    col_nav, col_content = st.columns([1, 3])
    with col_nav:
        st.markdown("##### CONSULTAS")
        escolha_menu = st.radio("Menu", list(CONSULTAS_INFO.keys()), label_visibility="collapsed")
    with col_content:
        dados = CONSULTAS_INFO[escolha_menu]
        sql_atual = dados["sql"]
        subtitulo = dados["subtitulo"]

        st.markdown(f"<h1 style='font-size: 2.5rem; color: #CC0000 !important; border: none; margin-bottom: 10px;'>{escolha_menu.upper()}</h1>", unsafe_allow_html=True)
        
        st.markdown(f"<p style='font-size: 1.1rem;'><span style='color: #3B4CCA; font-weight: bold;'>OBJETIVO:</span> {subtitulo}</p>", unsafe_allow_html=True)
        df = get_data(sql_atual)
        
        if not df.empty:
            t1, t2 = st.tabs(["GRÁFICOS", "TABELA DE DADOS"])
            with t2:
                st.dataframe(df, use_container_width=True)
                st.markdown("###### CÓDIGO SQL EXECUTADO:")
                st.code(sql_atual, language="sql")
            
            with t1:
                CORES_POKEMON = ['#CC0000', '#3B4CCA', '#B3A125', '#FFDE00', '#1E293B']
                fig = None
                
                if "Catálogo" in escolha_menu:
                    CORES_TREEMAP = [
                        '#CC0000', 
                        '#1E293B', 
                        '#B3A125', 
                        '#3B4CCA', 
                        '#D97706', 
                        '#15803D', 
                        '#0284C7'  
                    ]
                    
                    fig = px.treemap(
                        df, 
                        path=[df.columns[1], df.columns[2]],
                        color=df.columns[1], 
                        color_discrete_sequence=CORES_TREEMAP
                    )
                    fig.update_traces(
                        root_color="lightgrey",
                        textfont=dict(family="Coolvetica", size=20, color='#EEEEEE'),
                        textinfo="label+percent parent"
                    )
                    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

                elif "População" in escolha_menu or "Censo" in escolha_menu or "Total" in escolha_menu:
                    col_nome = df.columns[0]
                    col_valor = df.columns[1]
                    fig = px.pie(
                        df, names=col_nome, values=col_valor, 
                        hole=0.5, 
                        color_discrete_sequence=CORES_POKEMON
                    )
                    fig.update_traces(textinfo='value+percent')

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

with tab3:
    st.markdown("### MODELO CONCEITUAL")
    if os.path.exists("Conceitual_new.png"):
        st.markdown('<div class="tech-img">', unsafe_allow_html=True)
        st.image("Conceitual_new.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Imagem 'Conceitual_new.png' não encontrada no diretório.")

with tab4:
    st.markdown("### MODELO LÓGICO")
    if os.path.exists("Lógico_new.png"):
        st.markdown('<div class="tech-img">', unsafe_allow_html=True)
        st.image("Lógico_new.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Imagem 'Lógico_new.png' não encontrada no diretório.")

with tab5:
    st.markdown("### MODELO FÍSICO")
    codigo_sql = """
CREATE TABLE Geracao (
        Regiao VARCHAR(255),
        Numero INT PRIMARY KEY
    );

    CREATE TABLE Pokemon (
        Numero INT,
        Nome VARCHAR(255) PRIMARY KEY,
        HP INT,
        Defesa INT,
        Ataque INT,
        Ataque_Especial INT,
        Defesa_Especial INT,
        Velocidade INT,
        BST INT,
        idGeracao INT,
        FOREIGN KEY(idGeracao) REFERENCES Geracao (Numero)
    );

    CREATE TABLE Tipo (
        Imunidade VARCHAR(255),
        Nome VARCHAR(255) PRIMARY KEY,
        Nome_pt VARCHAR(255) UNIQUE
    );

    CREATE TABLE Habilidade (
        Nome VARCHAR(255) PRIMARY KEY,
        Descricao TEXT
    );

    CREATE TABLE Possui (
        Pokemon VARCHAR(255),
        Habilidade VARCHAR(255),
        PRIMARY KEY (Pokemon, Habilidade),
        FOREIGN KEY(Pokemon) REFERENCES Pokemon (Nome),
        FOREIGN KEY(Habilidade) REFERENCES Habilidade (Nome)
    );

    CREATE TABLE Pertence (
        Pokemon VARCHAR(255),
        Tipo VARCHAR(255),
        PRIMARY KEY (Pokemon, Tipo),
        FOREIGN KEY(Tipo) REFERENCES Tipo (Nome),
        FOREIGN KEY(Pokemon) REFERENCES Pokemon (Nome)
    );

    CREATE TABLE Efetividade (
        Multiplicador FLOAT,
        Atacante VARCHAR(255),
        Defensor VARCHAR(255),
        PRIMARY KEY (Atacante, Defensor),
        FOREIGN KEY(Atacante) REFERENCES Tipo (Nome),
        FOREIGN KEY(Defensor) REFERENCES Tipo (Nome)
    );

    """
    st.code(codigo_sql, language="sql")





