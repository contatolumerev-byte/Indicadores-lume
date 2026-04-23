import streamlit as st
from supabase import create_client, Client
import datetime

# --- CONFIGURAÇÃO DO SUPABASE ---
# Substitua pelos seus dados reais do painel do Supabase
url: str = "https://dhvekggpufraioiyszle.supabase.co"
key: str = "sb_publishable_h5Ot3KlVRXnFEmrGe2Lviw_kjsX4ErE"
supabase: Client = create_client(url, key)

# --- DICIONÁRIO MULTILÍNGUE (Governança Global) ---
languages = {
    'Português': {
        'title': 'Portal de Indicadores Shalom',
        'mission': 'Selecione a Missão',
        'area': 'Selecione a Área',
        'year': 'Ano de Referência',
        'confidence': 'Nível de Confiança do Dado',
        'options': ['Verificado (Sistema)', 'Planilha/Manual', 'Estimativa (Chute)'],
        'btn': 'Salvar Indicadores',
        'success': 'Dados enviados com sucesso para a base unificada!',
        'areas': ['Vocacional', 'Financeiro', 'Obras Sociais'],
        'metrics': {
            'Vocacional': ['Novos Engajados', 'Membros Ativos', 'Saídas'],
            'Financeiro': ['Arrecadação Total', 'Despesas Operacionais', 'Fundo de Missão'],
            'Obras Sociais': ['Atendimentos', 'Famílias Assistidas', 'Voluntários']
        }
    },
    'English': {
        'title': 'Shalom Indicators Portal',
        'mission': 'Select Mission',
        'area': 'Select Area',
        'year': 'Reference Year',
        'confidence': 'Data Confidence Level',
        'options': ['Verified (System)', 'Spreadsheet/Manual', 'Estimate (Guess)'],
        'btn': 'Save Indicators',
        'success': 'Data successfully sent to unified database!',
        'areas': ['Vocational', 'Financial', 'Social Works'],
        'metrics': {
            'Vocacional': ['New Engaged', 'Active Members', 'Departures'],
            'Financial': ['Total Revenue', 'Operating Expenses', 'Mission Fund'],
            'Social Works': ['Services Provided', 'Assisted Families', 'Volunteers']
        }
    },
    'Italiano': {
        'title': 'Portale degli Indicatori Shalom',
        'mission': 'Seleziona Missione',
        'area': 'Seleziona Area',
        'year': 'Anno di Riferimento',
        'confidence': 'Livello di Fiducia dei Dati',
        'options': ['Verificato', 'Manuale', 'Stima (Chute)'],
        'btn': 'Salva Indicatori',
        'success': 'Dati inviati con successo!',
        'areas': ['Vocazionale', 'Finanziario', 'Opere Sociali'],
        'metrics': {
            'Vocacional': ['Nuovi Impegnati', 'Membri Attivi', 'Uscite'],
            'Finanziario': ['Entrate Totali', 'Spese Operative', 'Fondo Missione'],
            'Opere Sociali': ['Servizi', 'Famiglie Assistite', 'Volontari']
        }
    }
    # Nota: Você pode expandir para FR, ES e DE seguindo o mesmo padrão.
}

# --- INTERFACE ---
st.set_page_config(page_title="Lume Rev | Shalom Global", page_icon="📊")

# Seletor de Idioma na Sidebar
lang_choice = st.sidebar.selectbox("🌍 Language / Idioma", list(languages.keys()))
lang = languages[lang_choice]

st.title(lang['title'])
st.markdown("---")

# --- FORMULÁRIO ---
with st.form("workflow_v1"):
    col1, col2 = st.columns(2)
    
    with col1:
        mission = st.text_input(lang['mission'], placeholder="Ex: Fortaleza / Roma")
        area = st.selectbox(lang['area'], lang['areas'])
        
    with col2:
        year = st.selectbox(lang['year'], [2024, 2025, 2026])
        confidence = st.selectbox(lang['confidence'], lang['options'])

    st.subheader(f"📊 {area}")
    
    # Busca os 3 indicadores específicos da área selecionada
    idx = lang['areas'].index(area)
    area_key_pt = languages['Português']['areas'][idx] # Chave fixa para o banco
    metrics = lang['metrics'][area]
    
    val1 = st.number_input(metrics[0], min_value=0)
    val2 = st.number_input(metrics[1], min_value=0)
    val3 = st.number_input(metrics[2], min_value=0)

    submitted = st.form_submit_button(lang['btn'])

    if submitted:
        # Preparação dos dados para o Supabase (Usando IDs fixos para o Looker Studio entender)
        data_to_save = [
            {"missao": mission, "area": area_key_pt, "indicador": metrics[0], "valor": val1, "ano": year, "confianca": confidence},
            {"missao": mission, "area": area_key_pt, "indicador": metrics[1], "valor": val2, "ano": year, "confianca": confidence},
            {"missao": mission, "area": area_key_pt, "indicador": metrics[2], "valor": val3, "ano": year, "confianca": confidence}
        ]
        
        try:
            # Envio para o Supabase
            supabase.table("historico_indicadores").insert(data_to_save).execute()
            st.success(lang['success'])
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao conectar com Supabase: {e}")

# --- RODAPÉ ESTRATÉGICO ---
st.sidebar.markdown("---")
st.sidebar.info(f"**Lume Rev Strategy**\n\nEste portal alimenta automaticamente as projeções de 5 anos no Looker Studio.")
import streamlit as st
from supabase import create_client, Client

# 1. CONEXÃO (Substitua pela sua KEY real que você já usou antes)
SUPABASE_URL = "https://dhvekggpufraioiyszle.supabase.co"
SUPABASE_KEY = "SUA_API_KEY_AQUI" 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. DICIONÁRIO MULTILÍNGUE (A "Pele" do App)
LANGUAGES = {
    "Português": {"mission": "Missão", "sector": "Setor Responsável", "ind": "Indicador", "val": "Valor", "conf": "Confiança", "btn": "Salvar", "msg": "Sucesso!"},
    "English": {"mission": "Mission", "sector": "Responsible Sector", "ind": "Indicator", "val": "Value", "conf": "Confidence", "btn": "Save", "msg": "Success!"},
    "Italiano": {"mission": "Missione", "sector": "Settore Responsabile", "ind": "Indicatore", "val": "Valore", "conf": "Fiducia", "btn": "Salvare", "msg": "Successo!"},
    "Español": {"mission": "Misión", "sector": "Sector Responsable", "ind": "Indicador", "val": "Valor", "conf": "Confianza", "btn": "Guardar", "msg": "¡Éxito!"},
    "Français": {"mission": "Mission", "sector": "Secteur Responsable", "ind": "Indicateur", "val": "Valeur", "conf": "Confiance", "btn": "Enregistrer", "msg": "Succès!"},
    "Deutsch": {"mission": "Mission", "sector": "Zuständiger Sektor", "ind": "Indikator", "val": "Wert", "conf": "Vertrauen", "btn": "Speichern", "msg": "Erfolgreich!"}
}

# 3. BASE DE INDICADORES (O "Coração" - Sempre em PT para o Looker)
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
        "Percentual de pessoas engajadas em ministérios"
    ],
    "Economato Geral": [
        "Índice de Sustentabilidade Econômica Missionária",
        "Percentual de membros que partilham a Comunhão de Bens",
        "Resultado operacional do setor"
    ],
    "Assessoria Jovem": [
        "Percentual de jovens na obra",
        "Quantidade de jovens em missão por ano",
        "Número de jovens que entram e permanecem nos grupos"
    ]
}

# 4. INTERFACE DO APP
st.set_page_config(page_title="Lume Rev Global", layout="centered")

# Seletor de Idioma
sel_lang = st.sidebar.selectbox("Language / Idioma", list(LANGUAGES.keys()))
lang = LANGUAGES[sel_lang]

st.title("Lume Rev")
st.subheader("Global Indicators Portal")

# Form de Entrada
missao = st.text_input(lang["mission"], placeholder="Ex: Fortaleza, Roma...")
setor_pt = st.selectbox(lang["sector"], list(DADOS_ESTRATEGICOS.keys()))
indicador_pt = st.selectbox(lang["ind"], DADOS_ESTRATEGICOS[setor_pt])

# Lógica de tipo de dado
is_percent = any(w in indicador_pt.lower() for w in ["taxa", "percentual", "porcentagem", "índice", "iqsa", "iqv"])

if is_percent:
    valor = st.number_input(f"{lang['val']} (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
    tipo_dado = "percentual"
else:
    valor = st.number_input(f"{lang['val']}", min_value=0, step=1)
    tipo_dado = "absoluto"

confianca = st.select_slider(lang["conf"], options=["Baixo", "Médio", "Alto"])

# 5. ENVIO PARA O SUPABASE
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
