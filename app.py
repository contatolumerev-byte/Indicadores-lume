import streamlit as st
from supabase import create_client, Client

# 1. CONEXÃO (Mantenha suas credenciais reais aqui)
SUPABASE_URL = "https://dhvekggpufraioiyszle.supabase.co"
SUPABASE_KEY = "SUA_API_KEY_AQUI" 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. DICIONÁRIO MULTILÍNGUE (Interface com 6 idiomas)
LANGUAGES = {
    "Português": {"mission": "Missão", "sector": "Setor Responsável", "ind": "Indicador", "val": "Valor", "conf": "Nível de Confiança do Dado", "btn": "Salvar Dados", "msg": "Dados salvos com sucesso!"},
    "English": {"mission": "Mission", "sector": "Responsible Sector", "ind": "Indicator", "val": "Value", "conf": "Data Confidence Level", "btn": "Save Data", "msg": "Data saved successfully!"},
    "Italiano": {"mission": "Missione", "sector": "Settore Responsabile", "ind": "Indicatore", "val": "Valore", "conf": "Livello di Fiducia dei Dati", "btn": "Salvare i Dati", "msg": "Dati salvati con successo!"},
    "Español": {"mission": "Misión", "sector": "Sector Responsable", "ind": "Indicador", "val": "Valor", "conf": "Nivel de Confianza de los Datos", "btn": "Guardar Datos", "msg": "¡Datos guardados con éxito!"},
    "Français": {"mission": "Mission", "sector": "Secteur Responsable", "ind": "Indicateur", "val": "Valeur", "conf": "Niveau de Confiance des Données", "btn": "Enregistrer", "msg": "Données enregistrées!"},
    "Deutsch": {"mission": "Mission", "sector": "Bereich", "ind": "Indikator", "val": "Wert", "conf": "Datenvertrauensniveau", "btn": "Speichern", "msg": "Erfolgreich gespeichert!"}
}

# Opções de confiança (Sua escala validada)
CONFIDENCE_OPTIONS = {
    "Português": ["Auditado (Sistema)", "Planilha de Controle", "Estimativa / Manual"],
    "English": ["Audited (System)", "Control Spreadsheet", "Estimation / Manual"],
    "Italiano": ["Auditato (Sistema)", "Foglio di Calcolo", "Stima / Manuale"],
    "Español": ["Auditado (Sistema)", "Planilla de Control", "Estimación / Manual"],
    "Français": ["Audité (Système)", "Feuille de Calcul", "Estimation / Manuel"],
    "Deutsch": ["Geprüft (System)", "Kontrollblatt", "Schätzung / Manuell"]
}

# 3. BASE DE INDICADORES (Sempre em PT para o Looker Studio)
DADOS_ESTRATEGICOS = {
    "Assistência Missionária": [
        "Taxa de crescimento de difusões em novas dioceses",
        "Taxa de fundações em novas dioceses",
        "Percentual da abertura de novas irradiações nas missões",
        "Evolução Média de Competência em Gestão Estratégica",
        "Índice de consolidação regional",
        "IQSA (Índice de Qualidade do Serviço de Autoridade)"
    ],
    "Assistência Apostólica": [
        "Percentual de aumento de pessoas alcançadas (Querigma)",
        "Número de membros no grupo de oração",
        "Taxa de permanência dos ingressantes após 6 meses",
        "Percentual de pessoas acompanhadas nos Grupos de Oração",
        "Percentual de pessoas engajadas em ministérios"
    ],
    "Economato Geral": [
        "Índice de Sustentabilidade Econômica Missionária",
        "Percentual de membros que partilham a Comunhão de Bens",
        "Resultado financeiro de doações (Valor Absoluto)"
    ]
    # Adicionaremos os demais conforme você validar
}

# 4. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Portal de Indicadores - Shalom", layout="centered")

# Barra Lateral - Seleção de Idioma
sel_lang = st.sidebar.selectbox("Idioma / Language", list(LANGUAGES.keys()))
lang = LANGUAGES[sel_lang]

# Título Principal (Protagonismo Shalom)
st.title("Portal de Indicadores Estratégicos")
st.markdown("### Comunidade Católica Shalom")

# Campo de Missão (Aguardando sua lista para virar Selectbox)
missao = st.text_input(lang["mission"], placeholder="Ex: Fortaleza, Roma, Berlin...")

# Seleção de Setor e Indicador
setor_pt = st.selectbox(lang["sector"], list(DADOS_ESTRATEGICOS.keys()))
indicador_pt = st.selectbox(lang["ind"], DADOS_ESTRATEGICOS[setor_pt])

# Lógica de Input
is_percent = any(w in indicador_pt.lower() for w in ["taxa", "percentual", "porcentagem", "índice", "iqsa"])

if is_percent:
    valor = st.number_input(f"{lang['val']} (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
    tipo_dado = "percentual"
else:
    valor = st.number_input(f"{lang['val']}", min_value=0, step=1)
    tipo_dado = "absoluto"

# Nível de Confiança do Dado
confianca = st.selectbox(lang["conf"], CONFIDENCE_OPTIONS[sel_lang])

# 5. BOTÃO DE ENVIO
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
        st.error(f"Erro ao salvar: {e}")

# Rodapé com assinatura da Consultoria (Lume Rev)
st.markdown("---")
st.caption("Implementado por Lume Rev Consultoria Estratégica")