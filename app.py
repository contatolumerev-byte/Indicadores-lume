import streamlit as st
from supabase import create_client, Client

# 1. CONEXÃO
SUPABASE_URL = "https://dhvekggpufraioiyszle.supabase.co"
SUPABASE_KEY = "SUA_API_KEY_AQUI" 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. DICIONÁRIO DE TRADUÇÃO DA INTERFACE E DOS SETORES
LANGUAGES = {
    "Português": {
        "mission": "Missão / Regional", "sector": "Setor Responsável", "ind": "Indicador", "val": "Valor", "conf": "Confiança", "btn": "Salvar", "msg": "Sucesso!",
        "setores": ["Assistência Missionária (Geral)", "Coordenação Apostólica (Missão)", "PJJ - Projeto Juventude (Missão)", "Secretaria Vocacional (Missão)", "Economato Local (Missão)", "Setores Produtivos"]
    },
    "English": {
        "mission": "Mission / Region", "sector": "Responsible Sector", "ind": "Indicator", "val": "Value", "conf": "Confidence", "btn": "Save", "msg": "Success!",
        "setores": ["Missionary Assistance (General)", "Apostolic Coordination (Mission)", "PJJ - Youth Project (Mission)", "Vocational Secretary (Mission)", "Local Finance (Mission)", "Productive Sectors"]
    },
    "Español": {
        "mission": "Misión / Regional", "sector": "Sector Responsable", "ind": "Indicador", "val": "Valor", "conf": "Confianza", "btn": "Guardar", "msg": "¡Éxito!",
        "setores": ["Asistencia Misionera (General)", "Coordinación Apostólica (Misión)", "PJJ - Proyecto Juventud (Misión)", "Secretaría Vocacional (Misión)", "Economía Local (Misión)", "Sectores Productivos"]
    },
    "Italiano": {
        "mission": "Missione", "sector": "Settore Responsabile", "ind": "Indicatore", "val": "Valore", "conf": "Fiducia", "btn": "Salvare", "msg": "Successo!",
        "setores": ["Assistenza Missionaria (Generale)", "Coordinamento Apostolico (Missione)", "PJJ - Progetto Gioventù (Missione)", "Segreteria Vocazionale (Missione)", "Economato Locale (Missione)", "Settori Produttivi"]
    },
    "Français": {
        "mission": "Mission", "sector": "Secteur Responsable", "ind": "Indicateur", "val": "Valeur", "conf": "Confiance", "btn": "Enregistrer", "msg": "Succès!",
        "setores": ["Assistance Missionnaire (Générale)", "Coordination Apostolique (Mission)", "PJJ - Projet Jeunesse (Mission)", "Secrétariat Vocationnel (Mission)", "Économat Local (Mission)", "Secteurs Productifs"]
    },
    "Deutsch": {
        "mission": "Mission", "sector": "Bereich", "ind": "Indikator", "val": "Wert", "conf": "Vertrauen", "btn": "Speichern", "msg": "Erfolgreich!",
        "setores": ["Missionarische Assistenz (Allgemein)", "Apostolische Koordination (Mission)", "PJJ - Jugendprojekt (Mission)", "Berufungssekretariat (Mission)", "Lokale Finanzen (Mission)", "Produktive Bereiche"]
    }
}

# 3. BASE DE DADOS (Chaves sempre em Português para o Looker)
INDICADORES_BASE = {
    "Assistência Missionária (Geral)": ["Taxa de crescimento de difusões", "Índice de consolidação regional", "IQSA"],
    "Coordenação Apostólica (Missão)": ["Número de membros no grupo de oração", "Taxa de permanência (6 meses)", "Engajamento em ministérios"],
    "PJJ - Projeto Juventude (Missão)": ["Percentual de jovens na obra", "Quantidade de jovens em missão por ano"],
    "Secretaria Vocacional (Missão)": ["Taxa de Crescimento de Ingressos", "Índice de Qualidade Vocacional (IQV)"],
    "Economato Local (Missão)": ["Resultado Operacional", "Membros na Comunhão de Bens"],
    "Setores Produtivos": ["Margem de contribuição (%)", "Taxa de crescimento do faturamento (%)"]
}

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Portal Shalom", layout="centered")

# Seleção de Idioma na Sidebar
sel_lang = st.sidebar.selectbox("Language / Idioma", list(LANGUAGES.keys()))
lang_dict = LANGUAGES[sel_lang]

st.title("Portal de Indicadores")
st.subheader("Comunidade Católica Shalom")

# CAMPOS TRADUZIDOS VISUALMENTE
missao = st.text_input(lang_dict["mission"])

# 1. Seleção do Setor (Mostra traduzido, mas mapeia para o PT)
lista_setores_traduzidos = lang_dict["setores"]
setor_selecionado_traduzido = st.selectbox(lang_dict["sector"], lista_setores_traduzidos)

# Descobre qual é o índice do setor selecionado para pegar a chave em PT
idx_setor = lista_setores_traduzidos.index(setor_selecionado_traduzido)
setor_chave_pt = list(INDICADORES_BASE.keys())[idx_setor]

# 2. Seleção do Indicador
indicador_pt = st.selectbox(lang_dict["ind"], INDICADORES_BASE[setor_chave_pt])

# Valor e Confiança
valor = st.number_input(lang_dict["val"], min_value=0.0)
confianca = st.selectbox(lang_dict["conf"], ["Auditado", "Planilha", "Manual"])

# ENVIO
if st.button(lang_dict["btn"]):
    payload = {
        "missao": missao,
        "setor": setor_chave_pt, # Salva em PT para o Looker
        "indicador": indicador_pt,
        "valor": valor,
        "idioma_preenchimento": sel_lang
    }
    try:
        supabase.table("historico_indicadores").insert(payload).execute()
        st.success(lang_dict["msg"])
    except Exception as e:
        st.error(f"Erro: {e}")
