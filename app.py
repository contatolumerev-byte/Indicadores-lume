import streamlit as st
from supabase import create_client, Client
import datetime

# --- CONFIGURAÇÃO DO SUPABASE ---
# Substitua pelos seus dados reais do painel do Supabase
url: str = "SUA_URL_DO_SUPABASE"
key: str = "SUA_API_KEY_DO_SUPABASE"
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
