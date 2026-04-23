import streamlit as st
from supabase import create_client, Client

# 1. CONEXÃO (Coloque suas chaves aqui)
SUPABASE_URL = "https://dhvekggpufraioiyszle.supabase.co"
SUPABASE_KEY = "SUA_API_KEY_REAL_AQUI" 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. CONFIGURAÇÃO VISUAL (Para não ficar em branco e ter a cara da Shalom)
st.set_page_config(page_title="Portal de Indicadores - Shalom", layout="centered", page_icon="📈")

# Estilização rápida para garantir que o texto apareça
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { width: 100%; background-color: #004a99; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. TRADUÇÕES (6 IDIOMAS)
LANGUAGES = {
    "Português": {"mission": "Missão / Regional", "sector": "Setor Responsável", "ind": "Indicador", "val": "Valor", "conf": "Confiança do Dado", "btn": "Salvar Dados", "msg": "Sucesso!"},
    "English": {"mission": "Mission", "sector": "Responsible Sector", "ind": "Indicator", "val": "Value", "conf": "Confidence", "btn": "Save Data", "msg": "Success!"},
    "Italiano": {"mission": "Missione", "sector": "Settore", "ind": "Indicatore", "val": "Valore", "conf": "Fiducia", "btn": "Salvare", "msg": "Successo!"},
    "Español": {"mission": "Misión", "sector": "Sector", "ind": "Indicador", "val": "Valor", "conf": "Confianza", "btn": "Guardar", "msg": "Éxito!"},
    "Français": {"mission": "Mission", "sector": "Secteur", "ind": "Indicateur", "val": "Valeur", "conf": "Confiance", "btn": "Enregistrer", "msg": "Succès!"},
    "Deutsch": {"mission": "Mission", "sector": "Bereich", "ind": "Indikator", "val": "Wert", "conf": "Vertrauen", "btn": "Speichern", "msg": "Erfolgreich!"}
}

# 4. BASE INTEGRAL DE INDICADORES (Ajustada com sua última lista)
DADOS_ESTRATEGICOS = {
    "Assistência Missionária (Geral)": [
        "Taxa de crescimento de difusões em novas dioceses", "Taxa de fundações em novas dioceses",
        "Percentual da abertura de novas irradiações", "Evolução Média de Competência em Gestão",
        "Índice de consolidação regional", "IQSA (Índice de Qualidade)", "Taxa de Execução do PDI (RLs)",
        "Relação Eclesial com Bispos"
    ],
    "Coordenação Apostólica (Missão)": [
        "Aumento de pessoas alcançadas (Querigma)", "Número de membros no grupo de oração",
        "Taxa de permanência (6 meses)", "Percentual de pessoas engajadas em ministérios",
        "Taxa de acolhimento nos CEVs", "Índice de engajamento integral"
    ],
    "PJJ - Projeto Juventude (Missão)": [
        "Percentual de jovens na obra", "Índice de alcance jovem nos veículos",
        "Jovens que entram e permanecem nos G.O.", "Quantidade de jovens em missão por ano"
    ],
    "Secretaria Vocacional (Missão)": [
        "Taxa de Crescimento no Número de Ingressos", "Índice de Qualidade Vocacional (IQV)",
        "Permanência até Promessas Definitivas"
    ],
    "Celibatários / Famílias / Sacerdotes": [
        "Celibatários CAL em missão", "Celibatários Nível 1 e 2",
        "Casais/Noivos Nível 1 e 2", "Índice de Consolidação Matrimonial",
        "Qualidade da vida de oração (Sacerdotes)"
    ],
    "Economato Local (Missão)": [
        "Sustentabilidade Econômica Missionária", "Resultado Operacional do Setor",
        "Contribuição para a Missão", "Membros na Comunhão de Bens",
        "Resultado financeiro de doações"
    ],
    "Promoção Humana / Parresia": [
        "Crescimento de pessoas assistidas", "Casas de PH fora do Brasil",
        "Crescimento de alunos ativos (Parresia)", "Membros da CV com Ensino Superior"
    ],
    "Tecnologia e Planejamento": [
        "Processos integrados ao sistema WOP", "Maturidade em gestão de dados",
        "Satisfação com processos institucionais"
    ],
    "Setores Produtivos (Livraria/Lanchonete)": [
        "Margem de contribuição (%)", "Taxa de crescimento do faturamento (%)"
    ]
}

# 5. LÓGICA DA INTERFACE
sel_lang = st.sidebar.selectbox("Idioma", list(LANGUAGES.keys()))
lang = LANGUAGES[sel_lang]

st.title("Portal de Indicadores")
st.subheader("Comunidade Católica Shalom")

missao = st.text_input(lang["mission"], placeholder="Ex: Parangaba - Fortaleza")

setor_pt = st.selectbox(lang["sector"], list(DADOS_ESTRATEGICOS.keys()))
indicador_pt = st.selectbox(lang["ind"], DADOS_ESTRATEGICOS[setor_pt])

# Detecção automática de tipo de dado
is_percent = any(w in indicador_pt.lower() for w in ["taxa", "percentual", "porcentagem", "índice", "iqsa", "iqv", "margem"])

if is_percent:
    valor = st.number_input(f"{lang['val']} (%)", min_value=0.0, max_value=500.0, step=0.1)
    tipo_dado = "percentual"
else:
    valor = st.number_input(lang["val"], min_value=0, step=1)
    tipo_dado = "absoluto"

confianca = st.selectbox(lang["conf"], ["Auditado (Sistema)", "Planilha de Controle", "Estimativa / Manual"])

# 6. ENVIO
if st.button(lang["btn"]):
    payload = {
        "missao": missao,
        "setor": setor_pt,
        "indicador": indicador_pt,
        "valor": valor,
        "tipo_dado": tipo_dado,
        "confianca": confianca,
        "idioma_preenchimento": sel_lang
    }
    
    try:
        supabase.table("historico_indicadores").insert(payload).execute()
        st.success(lang["msg"])
    except Exception as e:
        st.error(f"Erro: {e}")

st.markdown("---")
st.caption("Developed by Lume Rev Consultoria")
