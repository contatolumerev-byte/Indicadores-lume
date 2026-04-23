import streamlit as st
from supabase import create_client, Client

# 1. CONEXÃO (Mantenha suas chaves reais)
SUPABASE_URL = "https://dhvekggpufraioiyszle.supabase.co"
SUPABASE_KEY = "SUA_API_KEY_AQUI" 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. INTERFACE MULTILÍNGUE
LANGUAGES = {
    "Português": {"mission": "Missão / Regional", "sector": "Setor Responsável", "ind": "Indicador", "val": "Valor", "conf": "Confiança do Dado", "btn": "Salvar Dados", "msg": "Dados salvos com sucesso!"},
    "English": {"mission": "Mission / Regional", "sector": "Responsible Sector", "ind": "Indicator", "val": "Value", "conf": "Data Confidence", "btn": "Save Data", "msg": "Success!"},
    "Italiano": {"mission": "Missione", "sector": "Settore", "ind": "Indicatore", "val": "Valore", "conf": "Fiducia", "btn": "Salvare", "msg": "Successo!"},
    "Español": {"mission": "Misión", "sector": "Sector", "ind": "Indicador", "val": "Valor", "conf": "Confianza", "btn": "Guardar", "msg": "Éxito!"},
    "Français": {"mission": "Mission", "sector": "Secteur", "ind": "Indicateur", "val": "Valeur", "conf": "Confiance", "btn": "Enregistrer", "msg": "Succès!"},
    "Deutsch": {"mission": "Mission", "sector": "Bereich", "ind": "Indikator", "val": "Wert", "conf": "Vertrauen", "btn": "Speichern", "msg": "Erfolgreich!"}
}

CONFIDENCE_OPTIONS = {
    "Português": ["Auditado (Sistema)", "Planilha de Controle", "Estimativa / Manual"],
    "English": ["Audited (System)", "Control Spreadsheet", "Estimation / Manual"],
    "Italiano": ["Auditato (Sistema)", "Foglio di Calcolo", "Stima / Manuale"],
    "Español": ["Auditado (Sistema)", "Planilla de Control", "Estimación / Manual"],
    "Français": ["Audité (Système)", "Feuille de Calcul", "Estimation / Manuel"],
    "Deutsch": ["Geprüft (System)", "Kontrollblatt", "Schätzung / Manuell"]
}

# 3. MAPEAMENTO INTEGRAL DE TODOS OS INDICADORES (Hierarquia Missão vs Geral)
DADOS_ESTRATEGICOS = {
    "Assistência Missionária (Geral)": [
        "Taxa de crescimento de difusões em novas dioceses", "Taxa de fundações em novas dioceses",
        "Percentual da abertura de novas irradiações", "Evolução Média de Competência em Gestão",
        "Índice de consolidação regional", "IQSA (Índice de Qualidade do Serviço de Autoridade)",
        "Taxa de Execução do PDI (RLs)", "Percentual de Execução do Plano de Capacitações",
        "Índice de efetivação de novas autoridades", "Relação Eclesial com Bispos"
    ],
    "Coordenação Apostólica (Missão)": [
        "Aumento de pessoas alcançadas (Querigma)", "Número de membros no grupo de oração",
        "Taxa de permanência (6 meses)", "Percentual de pessoas acompanhadas nos G.O.",
        "Percentual de pessoas engajadas em ministérios", "Taxa de acolhimento nos CEVs",
        "Índice de engajamento integral dos membros", "Satisfação dos participantes do evento",
        "Novas iniciativas evangelizadoras", "Média da frequência de acompanhamento pessoal"
    ],
    "Projeto Juventude - PJJ (Missão)": [
        "Percentual de jovens na obra", "Índice de alcance jovem (Comshalom)",
        "Índice de qualidade dos eventos", "Crescimento de participantes em eventos",
        "Jovens que entram e permanecem nos G.O.", "Quantidade de jovens em missão por ano",
        "Atividades querigmáticas voltadas aos pobres"
    ],
    "Secretaria Vocacional (Missão)": [
        "Taxa de Crescimento no Número de Ingressos", "Índice de Qualidade Vocacional (IQV)",
        "Permanência até Promessas Definitivas"
    ],
    "Promoção Humana (Missão)": [
        "Crescimento de pessoas assistidas / reintegradas", "Casas de PH e missões com serviços fora do Brasil",
        "Percentual de Expedições realizadas"
    ],
    "Comunicação (Missão)": [
        "Tempo dedicado ao acolhimento digital", "Tempo médio de engajamento no Portal",
        "Satisfação do Serviço de Comunicação", "Índice de Treinamentos de Evangelização Digital"
    ],
    "Colegiado / Formação (Missão)": [
        "Adesão das ofertas formativas", "Acompanhamento Comunitário (AC) trimestral",
        "Irmãos que vivem os compromissos oracionais", "Engajamento da CAL",
        "Aplicação do novo modelo de atualização da CAL", "Celeiro de autoridades para a CAL"
    ],
    "Instituto Parresia": [
        "Crescimento de público em cursos presenciais", "Crescimento de alunos ativos",
        "Etapas executadas do projeto da Faculdade", "Membros da CV com Ensino Superior"
    ],
    "Responsável Local - RL (Missão)": [
        "Número de participantes em eventos formativos", "Contribuição dos setores produtivos na receita",
        "Índice de matrícula/permanência Colégio Shalom", "Avaliação geral dos CEVs"
    ],
    "Economato Local (Missão)": [
        "Sustentabilidade Econômica Missionária", "Resultado Operacional do Setor",
        "Contribuição para a Missão", "Membros na Comunhão de Bens",
        "Regularidade na prestação de contas", "Prática fiscal de comércio e serviço",
        "Resultado financeiro de doações (Valor Absoluto)", "Base Patrimonial Regularizada"
    ],
    "Secretaria Comunitária (Missão)": [
        "Pagamento do ordinário e dívida (Previdência)", "Índice de vivência da Unidade da CAL",
        "Membros assistidos por planos de saúde", "Índice de Qualidade de Vida Comunitária (IQVC)"
    ],
    "Tecnologia e Planejamento": [
        "Processos integrados ao sistema WOP", "Maturidade em gestão de dados",
        "Implantação do sistema integrado de gestão", "Satisfação com processos institucionais"
    ],
    "Celibatários / Famílias": [
        "Celibatários CAL que estão ou foram em missão", "Celibatários nos níveis vocacionais 1 e 2",
        "Casais/Noivos nos níveis vocacionais 1 e 2", "Índice de Consolidação Matrimonial"
    ],
    "Sacerdotes e Seminaristas": [
        "Qualidade da vida de oração e litúrgica", "Proporção nos níveis vocacionais 1 e 2"
    ],
    "Setores Produtivos (Livraria/Lanchonete)": [
        "Margem de contribuição (%)", "Taxa de crescimento do faturamento (%)"
    ]
}

# 4. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Portal de Indicadores - Shalom", layout="centered", page_icon="📈")

# Sidebar
sel_lang = st.sidebar.selectbox("Language / Idioma", list(LANGUAGES.keys()))
lang = LANGUAGES[sel_lang]

st.title("Portal de Indicadores")
st.markdown("### Comunidade Católica Shalom")

# Entrada da Missão
missao = st.text_input(lang["mission"], placeholder="Ex: Parangaba - Fortaleza")

# Dropdowns
setor_pt = st.selectbox(lang["sector"], list(DADOS_ESTRATEGICOS.keys()))
indicador_pt = st.selectbox(lang["ind"], DADOS_ESTRATEGICOS[setor_pt])

# Lógica de tipo de dado (Identifica automaticamente se é % ou Número)
is_percent = any(w in indicador_pt.lower() for w in ["taxa", "percentual", "porcentagem", "índice", "iqsa", "iqv", "margem", "evolução"])

if is_percent:
    valor = st.number_input(f"{lang['val']} (%)", min_value=0.0, max_value=500.0, step=0.1, format="%.1f")
    tipo_dado = "percentual"
else:
    valor = st.number_input(lang["val"], min_value=0, step=1)
    tipo_dado = "absoluto"

confianca = st.selectbox(lang["conf"], CONFIDENCE_OPTIONS[sel_lang])

# 5. SALVAMENTO
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
st.caption("Implementado por Lume Rev Consultoria Estratégica")
