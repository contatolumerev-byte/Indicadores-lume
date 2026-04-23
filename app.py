import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# 1. CONEXÃO
SUPABASE_URL = "https://dhvekggpufraioiyszle.supabase.co"
SUPABASE_KEY = "SUA_API_KEY_AQUI" 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. MAPEAMENTO MULTILÍNGUE: Cada idioma → Português (para o Looker)
# Estrutura: idioma → chave PT → valor no idioma
TRANSLATIONS = {
    "Português": {
        "title": "Portal de Indicadores Estratégicos",
        "subtitle": "Comunidade Católica Shalom",
        "mission_label": "Missão / Regional",
        "sector_label": "Setor Responsável",
        "indicator_label": "Indicador",
        "val_label": "Valor",
        "conf_label": "Confiança do Dado",
        "btn_save": "Salvar Dados",
        "msg_success": "Dados salvos com sucesso!",
        "sectors": {
            "Secretaria Vocacional (Missão)": "Secretaria Vocacional (Missão)",
            "Assistência Missionária (Geral)": "Assistência Missionária (Geral)",
            "PJJ - Projeto Juventude (Missão)": "PJJ - Projeto Juventude (Missão)"
        },
        "indicators": {
            "Taxa de Crescimento de Ingressos": "Taxa de Crescimento de Ingressos",
            "Percentual de jovens na obra": "Percentual de jovens na obra",
            "Índice de consolidação regional": "Índice de consolidação regional",
            "Índice de Qualidade Vocacional (IQV)": "Índice de Qualidade Vocacional (IQV)",
            "Quantidade de jovens em missão por ano": "Quantidade de jovens em missão por ano",
            "Taxa de crescimento de difusões": "Taxa de crescimento de difusões"
        },
        "confidence": {
            "Auditado": "Auditado",
            "Planilha": "Planilha",
            "Estimativa": "Estimativa"
        }
    },
    "English": {
        "title": "Strategic Indicators Portal",
        "subtitle": "Shalom Catholic Community",
        "mission_label": "Mission / Region",
        "sector_label": "Responsible Sector",
        "indicator_label": "Indicator",
        "val_label": "Value",
        "conf_label": "Data Confidence",
        "btn_save": "Save Data",
        "msg_success": "Data saved successfully!",
        "sectors": {
            "Secretaria Vocacional (Missão)": "Vocational Secretary (Mission)",
            "Assistência Missionária (Geral)": "Missionary Assistance (General)",
            "PJJ - Projeto Juventude (Missão)": "PJJ - Youth Project (Mission)"
        },
        "indicators": {
            "Taxa de Crescimento de Ingressos": "Growth Rate of New Members",
            "Percentual de jovens na obra": "Percentage of youth in the community",
            "Índice de consolidação regional": "Regional consolidation index",
            "Índice de Qualidade Vocacional (IQV)": "Vocational Quality Index (VQI)",
            "Quantidade de jovens em missão por ano": "Number of young people in mission per year",
            "Taxa de crescimento de difusões": "Growth rate of diffusions"
        },
        "confidence": {
            "Auditado": "Audited",
            "Planilha": "Spreadsheet",
            "Estimativa": "Estimate"
        }
    },
    "Español": {
        "title": "Portal de Indicadores Estratégicos",
        "subtitle": "Comunidad Católica Shalom",
        "mission_label": "Misión / Regional",
        "sector_label": "Sector Responsable",
        "indicator_label": "Indicador",
        "val_label": "Valor",
        "conf_label": "Confianza de los Datos",
        "btn_save": "Guardar Datos",
        "msg_success": "¡Datos guardados con éxito!",
        "sectors": {
            "Secretaria Vocacional (Missão)": "Secretaría Vocacional (Misión)",
            "Assistência Missionária (Geral)": "Asistencia Misionera (General)",
            "PJJ - Projeto Juventude (Missão)": "PJJ - Proyecto Juventud (Misión)"
        },
        "indicators": {
            "Taxa de Crescimento de Ingressos": "Tasa de Crecimiento de Ingresos",
            "Percentual de jovens na obra": "Porcentaje de jóvenes en la obra",
            "Índice de consolidação regional": "Índice de consolidación regional",
            "Índice de Qualidade Vocacional (IQV)": "Índice de Calidad Vocacional (ICV)",
            "Quantidade de jovens em missão por ano": "Cantidad de jóvenes en misión por año",
            "Taxa de crescimento de difusões": "Tasa de crecimiento de difusiones"
        },
        "confidence": {
            "Auditado": "Auditado",
            "Planilha": "Hoja de cálculo",
            "Estimativa": "Estimación"
        }
    },
    "Italiano": {
        "title": "Portale degli Indicatori Strategici",
        "subtitle": "Comunità Cattolica Shalom",
        "mission_label": "Missione / Regione",
        "sector_label": "Settore Responsabile",
        "indicator_label": "Indicatore",
        "val_label": "Valore",
        "conf_label": "Fiducia dei Dati",
        "btn_save": "Salva Dati",
        "msg_success": "Dati salvati con successo!",
        "sectors": {
            "Secretaria Vocacional (Missão)": "Segreteria Vocazionale (Missione)",
            "Assistência Missionária (Geral)": "Assistenza Missionaria (Generale)",
            "PJJ - Projeto Juventude (Missão)": "PJJ - Progetto Gioventù (Missione)"
        },
        "indicators": {
            "Taxa de Crescimento de Ingressos": "Tasso di Crescita dei Nuovi Membri",
            "Percentual de jovens na obra": "Percentuale di giovani nella comunità",
            "Índice de consolidação regional": "Indice di consolidamento regionale",
            "Índice de Qualidade Vocacional (IQV)": "Indice di Qualità Vocazionale (IQV)",
            "Quantidade de jovens em missão por ano": "Numero di giovani in missione per anno",
            "Taxa de crescimento de difusões": "Tasso di crescita delle diffusioni"
        },
        "confidence": {
            "Auditado": "Revisionato",
            "Planilha": "Foglio di calcolo",
            "Estimativa": "Stima"
        }
    },
    "Français": {
        "title": "Portail des Indicateurs Stratégiques",
        "subtitle": "Communauté Catholique Shalom",
        "mission_label": "Mission / Région",
        "sector_label": "Secteur Responsable",
        "indicator_label": "Indicateur",
        "val_label": "Valeur",
        "conf_label": "Confiance des Données",
        "btn_save": "Enregistrer les Données",
        "msg_success": "Données enregistrées avec succès!",
        "sectors": {
            "Secretaria Vocacional (Missão)": "Secrétariat Vocationnel (Mission)",
            "Assistência Missionária (Geral)": "Assistance Missionnaire (Générale)",
            "PJJ - Projeto Juventude (Missão)": "PJJ - Projet Jeunesse (Mission)"
        },
        "indicators": {
            "Taxa de Crescimento de Ingressos": "Taux de Croissance des Nouveaux Membres",
            "Percentual de jovens na obra": "Pourcentage de jeunes dans la communauté",
            "Índice de consolidação regional": "Indice de consolidation régionale",
            "Índice de Qualidade Vocacional (IQV)": "Indice de Qualité Vocationnelle (IQV)",
            "Quantidade de jovens em missão por ano": "Nombre de jeunes en mission par an",
            "Taxa de crescimento de difusões": "Taux de croissance des diffusions"
        },
        "confidence": {
            "Auditado": "Audité",
            "Planilha": "Feuille de calcul",
            "Estimativa": "Estimation"
        }
    },
    "Deutsch": {
        "title": "Portal der strategischen Indikatoren",
        "subtitle": "Shalom Katholische Gemeinschaft",
        "mission_label": "Mission / Region",
        "sector_label": "Verantwortlicher Sektor",
        "indicator_label": "Indikator",
        "val_label": "Wert",
        "conf_label": "Datenvertrauen",
        "btn_save": "Daten Speichern",
        "msg_success": "Daten erfolgreich gespeichert!",
        "sectors": {
            "Secretaria Vocacional (Missão)": "Berufungssekretariat (Mission)",
            "Assistência Missionária (Geral)": "Missionarische Hilfe (Allgemein)",
            "PJJ - Projeto Juventude (Missão)": "PJJ - Jugendprojekt (Mission)"
        },
        "indicators": {
            "Taxa de Crescimento de Ingressos": "Wachstumssatz neuer Mitglieder",
            "Percentual de jovens na obra": "Prozentsatz der Jugendlichen in der Gemeinschaft",
            "Índice de consolidação regional": "Regionalkonsolidierungsindex",
            "Índice de Qualidade Vocacional (IQV)": "Berufungsqualitätsindex (BQI)",
            "Quantidade de jovens em missão por ano": "Anzahl junger Menschen in der Mission pro Jahr",
            "Taxa de crescimento de difusões": "Wachstumsrate der Diffusionen"
        },
        "confidence": {
            "Auditado": "Geprüft",
            "Planilha": "Tabellenkalkulation",
            "Estimativa": "Schätzung"
        }
    }
}

# 3. ESTRUTURA DO BANCO (chaves em Português - isto é o que o Looker vê)
DB_STRUCTURE_PT = {
    "Secretaria Vocacional (Missão)": [
        "Taxa de Crescimento de Ingressos",
        "Índice de Qualidade Vocacional (IQV)"
    ],
    "PJJ - Projeto Juventude (Missão)": [
        "Percentual de jovens na obra",
        "Quantidade de jovens em missão por ano"
    ],
    "Assistência Missionária (Geral)": [
        "Índice de consolidação regional",
        "Taxa de crescimento de difusões"
    ]
}

# CONFIGURAÇÃO DO APP
st.set_page_config(page_title="Shalom Indicators", layout="centered")

# SIDEBAR - Seleção de Idioma
sel_lang = st.sidebar.selectbox("🌍 Language / Idioma", list(TRANSLATIONS.keys()))
t = TRANSLATIONS[sel_lang]

# INTERFACE TRADUZIDA
st.title(t["title"])
st.subheader(t["subtitle"])
st.markdown("---")

missao = st.text_input(t["mission_label"])

# SELEÇÃO DE SETOR (em Português na chave, traduzido para o usuário)
setores_pt_keys = list(DB_STRUCTURE_PT.keys())
setores_display = [t["sectors"][setor_pt] for setor_pt in setores_pt_keys]

idx_setor = st.selectbox(t["sector_label"], range(len(setores_display)), 
                         format_func=lambda x: setores_display[x])
setor_pt = setores_pt_keys[idx_setor]

# SELEÇÃO DE INDICADOR (em Português na chave, traduzido para o usuário)
indicadores_pt = DB_STRUCTURE_PT[setor_pt]
indicadores_display = [t["indicators"][ind_pt] for ind_pt in indicadores_pt]

idx_ind = st.selectbox(t["indicator_label"], range(len(indicadores_display)), 
                       format_func=lambda x: indicadores_display[x])
indicador_pt = indicadores_pt[idx_ind]

# VALOR E CONFIANÇA
valor = st.number_input(t["val_label"], min_value=0.0)

confianca_keys = list(t["confidence"].keys())
idx_conf = st.selectbox(t["conf_label"], range(len(confianca_keys)), 
                        format_func=lambda x: t["confidence"][confianca_keys[x]])
confianca_pt = confianca_keys[idx_conf]

# BOTÃO SALVAR
if st.button(t["btn_save"]):
    payload = {
        "missao": missao,
        "setor": setor_pt,           # ✅ Em Português para o Looker
        "indicador": indicador_pt,   # ✅ Em Português para o Looker
        "valor": valor,
        "confianca": confianca_pt,   # ✅ Em Português para o Looker
        "idioma_preenchimento": sel_lang,
        "data_preenchimento": datetime.now().isoformat()
    }
    try:
        supabase.table("historico_indicadores").insert(payload).execute()
        st.success(t["msg_success"])
    except Exception as e:
        st.error(f"Error: {e}")
