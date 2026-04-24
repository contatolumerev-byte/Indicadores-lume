import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import pandas as pd

# 1. CONEXÃO
SUPABASE_URL = "https://dhvekggpufraioiyszle.supabase.co"
SUPABASE_KEY = "SUA_API_KEY_AQUI" 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. ESTRUTURA DE MISSÕES POR REGIONAL
MISSOES_PT = {
    "Diaconia - Governo Geral": ["Fortaleza"],
    
    "Regional Brasil Nordeste I": [
        "Teresina (Sede)",
        "Crateús",
        "Parnaíba",
        "Itapipoca",
        "Sobral",
        "Aracati",
        "Quixadá",
        "São Luís",
        "Imperatriz",
        "Juazeiro do Norte"
    ],
    
    "Regional Brasil Nordeste II": [
        "Salvador (Sede)",
        "Natal",
        "Mossoró",
        "Patos",
        "Recife",
        "Garanhuns",
        "Maceió",
        "Arapiraca",
        "João Pessoa",
        "Campina Grande",
        "Juazeiro - BA",
        "Vitória da Conquista/BA",
        "Aracaju",
        "Petrolina",
        "Propriá",
        "Senhor do Bonfim",
        "Eunápolis"
    ],
    
    "Regional Brasil Norte": [
        "Belém (Sede)",
        "Chaves",
        "Cruzeiro do Sul",
        "Macapá",
        "Manaus"
    ],
    
    "Regional Brasil Sudeste e Centro-Oeste": [
        "Brasília (Sede)",
        "Goiânia",
        "Cuiabá",
        "Campo Grande",
        "Palmas",
        "Rio de Janeiro",
        "Niterói",
        "Campos",
        "Juiz de Fora",
        "Vitória",
        "Belo Horizonte",
        "Patos de Minas",
        "Uberaba"
    ],
    
    "Regional Brasil São Paulo": [
        "São Paulo (Sede)",
        "Santo Amaro",
        "Aparecida",
        "Araraquara",
        "Guarulhos",
        "Santo André",
        "Piracicaba"
    ],
    
    "Regional Brasil Sul": [
        "Curitiba (Sede)",
        "Joinville",
        "Florianópolis",
        "Ponta Grossa",
        "São Leopoldo"
    ],
    
    "Regional América Hispânica": [
        "Assunção (Sede)",
        "Montevidéu",
        "Sucre",
        "Corrientes",
        "Lima",
        "Guayaquil",
        "Bogotá",
        "Santa Cruz de la Sierra",
        "Cidade do Panamá",
        "Santiago do Chile"
    ],
    
    "Regional Europa": [
        "Roma",
        "Ferrara",
        "Acqui Terme",
        "Lugano",
        "Granada",
        "Braga",
        "Setúbal",
        "Lisboa",
        "Toulon",
        "Aix-en-Provence",
        "Avignon",
        "Guiana Francesa",
        "Perpignan",
        "Nice",
        "Varsóvia",
        "Cracóvia",
        "Budapeste",
        "Paderborn",
        "Londres"
    ],
    
    "Regional Ásia": [
        "Haifa (Sede)",
        "Nazaré",
        "Manila (Filipinas)",
        "Hsinchu (Taiwan)"
    ],
    
    "Regional África": [
        "Maputo (Sede)",
        "Praia (Cabo Verde)",
        "Lubango",
        "Madagascar",
        "Argel",
        "Béjaia",
        "Sfax",
        "Tânger"
    ],
    
    "Regional América do Norte": [
        "Nova Iorque (Sede)",
        "Boston",
        "Toronto"
    ]
}

# 3. FUNÇÃO PARA DETECTAR FORMATO DO INDICADOR
def detect_indicator_format(indicator_name):
    """
    Detecta o formato do indicador baseado no nome
    % = Taxa, Percentual, Índice, Porcentagem, Margem
    # = Número, Quantidade
    $ = Resultado, Valor, Financeiro
    """
    indicator_lower = indicator_name.lower()
    
    if any(word in indicator_lower for word in ["taxa", "percentual", "índice", "porcentagem", "margem", "proporção"]):
        return "%"
    elif any(word in indicator_lower for word in ["número", "quantidade"]):
        return "#"
    elif any(word in indicator_lower for word in ["resultado", "valor", "financeiro"]):
        return "$"
    else:
        return "%"

# 4. MAPEAMENTO MULTILÍNGUE
TRANSLATIONS = {
    "Português": {
        "title": "Portal de Indicadores Estratégicos",
        "subtitle": "Comunidade Católica Shalom",
        "regional_label": "Regional",
        "mission_label": "Missão",
        "year_label": "Ano",
        "sector_label": "Assessoria / Assistência",
        "indicator_label": "Indicador",
        "val_label": "Valor",
        "conf_label": "Confiança do Dado",
        "btn_save": "Salvar Dados",
        "btn_correct": "🔄 Corrigir",
        "btn_history": "📋 Histórico",
        "btn_confirm_correct": "✅ Confirmar Correção",
        "btn_cancel": "❌ Cancelar",
        "msg_success": "Dados salvos com sucesso!",
        "msg_success_correct": "✅ Correção registrada com sucesso!",
        "msg_already_filled": "⚠️ Este indicador para {ano} já foi preenchido!",
        "msg_pending": "✅ Este indicador está pendente. Pode preencher!",
        "confidence_options": ["Sistema", "Planilha", "Chute/Estimativa"],
        "correction_reasons": ["Erro de Digitação", "Dado Atualizado", "Revisão de Dados", "Outro"],
        "regions": {
            "Diaconia - Governo Geral": "Diaconia - Governo Geral",
            "Regional Brasil Nordeste I": "Regional Brasil Nordeste I",
            "Regional Brasil Nordeste II": "Regional Brasil Nordeste II",
            "Regional Brasil Norte": "Regional Brasil Norte",
            "Regional Brasil Sudeste e Centro-Oeste": "Regional Brasil Sudeste e Centro-Oeste",
            "Regional Brasil São Paulo": "Regional Brasil São Paulo",
            "Regional Brasil Sul": "Regional Brasil Sul",
            "Regional América Hispânica": "Regional América Hispânica",
            "Regional Europa": "Regional Europa",
            "Regional Ásia": "Regional Ásia",
            "Regional África": "Regional África",
            "Regional América do Norte": "Regional América do Norte"
        },
        "sectors": {
            "Assistência Missionária": "Assistência Missionária",
            "Assistência Apostólica": "Assistência Apostólica",
            "Assessoria Jovem": "Assessoria Jovem",
            "Assessoria Vocacional": "Assessoria Vocacional",
            "Assessoria de Promoção Humana": "Assessoria de Promoção Humana",
            "Assistência de Formação": "Assistência de Formação",
            "Economato Geral": "Economato Geral",
            "Assistência Internacional": "Assistência Internacional",
            "Escritório Geral": "Escritório Geral",
            "Assistência Comunitária": "Assistência Comunitária",
            "Assessoria Litúrgico-Sacramental": "Assessoria Litúrgico-Sacramental",
            "Assistência de Comunicação": "Assistência de Comunicação",
            "Secretaria de Tecnologia": "Secretaria de Tecnologia",
            "Secretaria de Planejamento e Gestão": "Secretaria de Planejamento e Gestão",
            "Assistência Local": "Assistência Local",
            "Instituto Parresia": "Instituto Parresia",
            "Secretaria dos Sacerdotes e Seminaristas": "Secretaria dos Sacerdotes e Seminaristas",
            "Setor dos Celibatários": "Setor dos Celibatários",
            "Setor Família": "Setor Família",
            "Secretaria de Setores Produtivos": "Secretaria de Setores Produtivos"
        }
    },
    "English": {
        "title": "Strategic Indicators Portal",
        "subtitle": "Shalom Catholic Community",
        "regional_label": "Region",
        "mission_label": "Mission",
        "year_label": "Year",
        "sector_label": "Department / Assistance",
        "indicator_label": "Indicator",
        "val_label": "Value",
        "conf_label": "Data Confidence",
        "btn_save": "Save Data",
        "btn_correct": "🔄 Correct",
        "btn_history": "📋 History",
        "btn_confirm_correct": "✅ Confirm Correction",
        "btn_cancel": "❌ Cancel",
        "msg_success": "Data saved successfully!",
        "msg_success_correct": "✅ Correction recorded successfully!",
        "msg_already_filled": "⚠️ This indicator for {ano} has already been filled!",
        "msg_pending": "✅ This indicator is pending. You can fill it!",
        "confidence_options": ["System", "Spreadsheet", "Guess/Estimate"],
        "correction_reasons": ["Typing Error", "Updated Data", "Data Review", "Other"],
        "regions": {
            "Diaconia - Governo Geral": "Diaconia - General Government",
            "Regional Brasil Nordeste I": "Brazil Northeast I Region",
            "Regional Brasil Nordeste II": "Brazil Northeast II Region",
            "Regional Brasil Norte": "Brazil North Region",
            "Regional Brasil Sudeste e Centro-Oeste": "Brazil Southeast and Center-West Region",
            "Regional Brasil São Paulo": "Brazil São Paulo Region",
            "Regional Brasil Sul": "Brazil South Region",
            "Regional América Hispânica": "Hispanic America Region",
            "Regional Europa": "Europe Region",
            "Regional Ásia": "Asia Region",
            "Regional África": "Africa Region",
            "Regional América do Norte": "North America Region"
        },
        "sectors": {
            "Assistência Missionária": "Missionary Assistance",
            "Assistência Apostólica": "Apostolic Assistance",
            "Assessoria Jovem": "Youth Advisory",
            "Assessoria Vocacional": "Vocational Advisory",
            "Assessoria de Promoção Humana": "Human Promotion Advisory",
            "Assistência de Formação": "Formation Assistance",
            "Economato Geral": "General Economic Management",
            "Assistência Internacional": "International Assistance",
            "Escritório Geral": "General Office",
            "Assistência Comunitária": "Community Assistance",
            "Assessoria Litúrgico-Sacramental": "Liturgical-Sacramental Advisory",
            "Assistência de Comunicação": "Communication Assistance",
            "Secretaria de Tecnologia": "Technology Secretariat",
            "Secretaria de Planejamento e Gestão": "Planning and Management Secretariat",
            "Assistência Local": "Local Assistance",
            "Instituto Parresia": "Parresia Institute",
            "Secretaria dos Sacerdotes e Seminaristas": "Secretariat of Priests and Seminarians",
            "Setor dos Celibatários": "Celibate Sector",
            "Setor Família": "Family Sector",
            "Secretaria de Setores Produtivos": "Productive Sectors Secretariat"
        }
    },
    "Español": {
        "title": "Portal de Indicadores Estratégicos",
        "subtitle": "Comunidad Católica Shalom",
        "regional_label": "Región",
        "mission_label": "Misión",
        "year_label": "Año",
        "sector_label": "Departamento / Asistencia",
        "indicator_label": "Indicador",
        "val_label": "Valor",
        "conf_label": "Confianza de los Datos",
        "btn_save": "Guardar Datos",
        "btn_correct": "🔄 Corregir",
        "btn_history": "📋 Historial",
        "btn_confirm_correct": "✅ Confirmar Corrección",
        "btn_cancel": "❌ Cancelar",
        "msg_success": "¡Datos guardados con éxito!",
        "msg_success_correct": "✅ ¡Corrección registrada con éxito!",
        "msg_already_filled": "⚠️ ¡Este indicador para {ano} ya ha sido completado!",
        "msg_pending": "✅ Este indicador está pendiente. ¡Puede rellenarlo!",
        "confidence_options": ["Sistema", "Hoja de cálculo", "Estimación"],
        "correction_reasons": ["Error de Tipeo", "Dato Actualizado", "Revisión de Datos", "Otro"],
        "regions": {
            "Diaconia - Governo Geral": "Diaconia - Gobierno General",
            "Regional Brasil Nordeste I": "Región Noreste de Brasil I",
            "Regional Brasil Nordeste II": "Región Noreste de Brasil II",
            "Regional Brasil Norte": "Región Norte de Brasil",
            "Regional Brasil Sudeste e Centro-Oeste": "Región Sureste y Centro-Oeste de Brasil",
            "Regional Brasil São Paulo": "Región São Paulo de Brasil",
            "Regional Brasil Sul": "Región Sur de Brasil",
            "Regional América Hispânica": "Región América Hispánica",
            "Regional Europa": "Región Europa",
            "Regional Ásia": "Región Asia",
            "Regional África": "Región África",
            "Regional América do Norte": "Región América del Norte"
        },
        "sectors": {
            "Assistência Missionária": "Asistencia Misionera",
            "Assistência Apostólica": "Asistencia Apostólica",
            "Assessoria Jovem": "Asesoría de Jóvenes",
            "Assessoria Vocacional": "Asesoría Vocacional",
            "Assessoria de Promoção Humana": "Asesoría de Promoción Humana",
            "Assistência de Formação": "Asistencia de Formación",
            "Economato Geral": "Economía General",
            "Assistência Internacional": "Asistencia Internacional",
            "Escritório Geral": "Oficina General",
            "Assistência Comunitária": "Asistencia Comunitaria",
            "Assessoria Litúrgico-Sacramental": "Asesoría Litúrgico-Sacramental",
            "Assistência de Comunicação": "Asistencia de Comunicación",
            "Secretaria de Tecnologia": "Secretaría de Tecnología",
            "Secretaria de Planejamento e Gestão": "Secretaría de Planificación y Gestión",
            "Assistência Local": "Asistencia Local",
            "Instituto Parresia": "Instituto Parresia",
            "Secretaria dos Sacerdotes e Seminaristas": "Secretaría de Sacerdotes y Seminaristas",
            "Setor dos Celibatários": "Sector de Célibes",
            "Setor Família": "Sector Familiar",
            "Secretaria de Setores Produtivos": "Secretaría de Sectores Productivos"
        }
    },
    "Italiano": {
        "title": "Portale degli Indicatori Strategici",
        "subtitle": "Comunità Cattolica Shalom",
        "regional_label": "Regione",
        "mission_label": "Missione",
        "year_label": "Anno",
        "sector_label": "Dipartimento / Assistenza",
        "indicator_label": "Indicatore",
        "val_label": "Valore",
        "conf_label": "Fiducia dei Dati",
        "btn_save": "Salva Dati",
        "btn_correct": "🔄 Correggi",
        "btn_history": "📋 Storico",
        "btn_confirm_correct": "✅ Conferma Correzione",
        "btn_cancel": "❌ Annulla",
        "msg_success": "Dati salvati con successo!",
        "msg_success_correct": "✅ Correzione registrata con successo!",
        "msg_already_filled": "⚠️ Questo indicatore per {ano} è già stato compilato!",
        "msg_pending": "✅ Questo indicatore è in sospeso. Puoi compilarlo!",
        "confidence_options": ["Sistema", "Foglio di calcolo", "Stima"],
        "correction_reasons": ["Errore di Digitazione", "Dati Aggiornati", "Revisione Dati", "Altro"],
        "regions": {
            "Diaconia - Governo Geral": "Diaconia - Governo Generale",
            "Regional Brasil Nordeste I": "Regione Nord-Est Brasile I",
            "Regional Brasil Nordeste II": "Regione Nord-Est Brasile II",
            "Regional Brasil Norte": "Regione Nord Brasile",
            "Regional Brasil Sudeste e Centro-Oeste": "Regione Sud-Est e Centro-Ovest Brasile",
            "Regional Brasil São Paulo": "Regione São Paulo Brasile",
            "Regional Brasil Sul": "Regione Sud Brasile",
            "Regional América Hispânica": "Regione America Ispanica",
            "Regional Europa": "Regione Europa",
            "Regional Ásia": "Regione Asia",
            "Regional África": "Regione Africa",
            "Regional América do Norte": "Regione America del Nord"
        },
        "sectors": {
            "Assistência Missionária": "Assistenza Missionaria",
            "Assistência Apostólica": "Assistenza Apostolica",
            "Assessoria Jovem": "Consulenza per i Giovani",
            "Assessoria Vocacional": "Consulenza Vocazionale",
            "Assessoria de Promoção Humana": "Consulenza per la Promozione Umana",
            "Assistência de Formação": "Assistenza alla Formazione",
            "Economato Geral": "Economia Generale",
            "Assistência Internacional": "Assistenza Internazionale",
            "Escritório Geral": "Ufficio Generale",
            "Assistência Comunitária": "Assistenza Comunitaria",
            "Assessoria Litúrgico-Sacramental": "Consulenza Liturgico-Sacramentale",
            "Assistência de Comunicação": "Assistenza alla Comunicazione",
            "Secretaria de Tecnologia": "Segreteria della Tecnologia",
            "Secretaria de Planejamento e Gestão": "Segreteria della Pianificazione e Gestione",
            "Assistência Local": "Assistenza Locale",
            "Instituto Parresia": "Istituto Parresia",
            "Secretaria dos Sacerdotes e Seminaristas": "Segreteria dei Sacerdoti e Seminaristi",
            "Setor dos Celibatários": "Settore dei Celibi",
            "Setor Família": "Settore Famiglia",
            "Secretaria de Setores Produtivos": "Segreteria dei Settori Produttivi"
        }
    },
    "Français": {
        "title": "Portail des Indicateurs Stratégiques",
        "subtitle": "Communauté Catholique Shalom",
        "regional_label": "Région",
        "mission_label": "Mission",
        "year_label": "Année",
        "sector_label": "Département / Assistance",
        "indicator_label": "Indicateur",
        "val_label": "Valeur",
        "conf_label": "Confiance des Données",
        "btn_save": "Enregistrer les Données",
        "btn_correct": "🔄 Corriger",
        "btn_history": "📋 Historique",
        "btn_confirm_correct": "✅ Confirmer la Correction",
        "btn_cancel": "❌ Annuler",
        "msg_success": "Données enregistrées avec succès!",
        "msg_success_correct": "✅ Correction enregistrée avec succès!",
        "msg_already_filled": "⚠️ Cet indicateur pour {ano} a déjà été rempli!",
        "msg_pending": "✅ Cet indicateur est en attente. Vous pouvez le remplir!",
        "confidence_options": ["Système", "Feuille de calcul", "Estimation"],
        "correction_reasons": ["Erreur de Saisie", "Données Mises à Jour", "Révision des Données", "Autre"],
        "regions": {
            "Diaconia - Governo Geral": "Diaconia - Gouvernement Général",
            "Regional Brasil Nordeste I": "Région Nord-Est Brésil I",
            "Regional Brasil Nordeste II": "Région Nord-Est Brésil II",
            "Regional Brasil Norte": "Région Nord Brésil",
            "Regional Brasil Sudeste e Centro-Oeste": "Région Sud-Est et Centre-Ouest Brésil",
            "Regional Brasil São Paulo": "Région São Paulo Brésil",
            "Regional Brasil Sul": "Région Sud Brésil",
            "Regional América Hispânica": "Région Amérique Hispanique",
            "Regional Europa": "Région Europe",
            "Regional Ásia": "Région Asie",
            "Regional África": "Région Afrique",
            "Regional América do Norte": "Région Amérique du Nord"
        },
        "sectors": {
            "Assistência Missionária": "Assistance Missionnaire",
            "Assistência Apostólica": "Assistance Apostolique",
            "Assessoria Jovem": "Conseil Jeunesse",
            "Assessoria Vocacional": "Conseil Vocationnel",
            "Assessoria de Promoção Humana": "Conseil pour la Promotion Humaine",
            "Assistência de Formação": "Assistance à la Formation",
            "Economato Geral": "Économie Générale",
            "Assistência Internacional": "Assistance Internationale",
            "Escritório Geral": "Bureau Général",
            "Assistência Comunitária": "Assistance Communautaire",
            "Assessoria Litúrgico-Sacramental": "Conseil Liturgique-Sacramentel",
            "Assistência de Comunicação": "Assistance à la Communication",
            "Secretaria de Tecnologia": "Secrétariat de la Technologie",
            "Secretaria de Planejamento e Gestão": "Secrétariat de la Planification et de la Gestion",
            "Assistência Local": "Assistance Locale",
            "Instituto Parresia": "Institut Parresia",
            "Secretaria dos Sacerdotes e Seminaristas": "Secrétariat des Prêtres et Séminaristes",
            "Setor dos Celibatários": "Secteur des Célibataires",
            "Setor Família": "Secteur Famille",
            "Secretaria de Setores Produtivos": "Secrétariat des Secteurs Productifs"
        }
    },
    "Deutsch": {
        "title": "Portal der strategischen Indikatoren",
        "subtitle": "Shalom Katholische Gemeinschaft",
        "regional_label": "Region",
        "mission_label": "Mission",
        "year_label": "Jahr",
        "sector_label": "Abteilung / Hilfe",
        "indicator_label": "Indikator",
        "val_label": "Wert",
        "conf_label": "Datenvertrauen",
        "btn_save": "Daten Speichern",
        "btn_correct": "🔄 Korrigieren",
        "btn_history": "📋 Verlauf",
        "btn_confirm_correct": "✅ Korrektur Bestätigen",
        "btn_cancel": "❌ Abbrechen",
        "msg_success": "Daten erfolgreich gespeichert!",
        "msg_success_correct": "✅ Korrektur erfolgreich registriert!",
        "msg_already_filled": "⚠️ Dieser Indikator für {ano} wurde bereits ausgefüllt!",
        "msg_pending": "✅ Dieser Indikator ist ausstehend. Sie können ihn ausfüllen!",
        "confidence_options": ["System", "Tabellenkalkulation", "Schätzung"],
        "correction_reasons": ["Tippfehler", "Aktualisierte Daten", "Datenüberprüfung", "Sonstiges"],
        "regions": {
            "Diaconia - Governo Geral": "Diaconia - Allgemeine Regierung",
            "Regional Brasil Nordeste I": "Region Nordost-Brasilien I",
            "Regional Brasil Nordeste II": "Region Nordost-Brasilien II",
            "Regional Brasil Norte": "Region Nord-Brasilien",
            "Regional Brasil Sudeste e Centro-Oeste": "Region Südosten und Mittenwesten Brasilien",
            "Regional Brasil São Paulo": "Region São Paulo Brasilien",
            "Regional Brasil Sul": "Region Süd-Brasilien",
            "Regional América Hispânica": "Region Hispanoamerika",
            "Regional Europa": "Region Europa",
            "Regional Ásia": "Region Asien",
            "Regional África": "Region Afrika",
            "Regional América do Norte": "Region Nordamerika"
        },
        "sectors": {
            "Assistência Missionária": "Missionarische Hilfe",
            "Assistência Apostólica": "Apostolische Hilfe",
            "Assessoria Jovem": "Jugendberatung",
            "Assessoria Vocacional": "Berufungsberatung",
            "Assessoria de Promoção Humana": "Beratung für Menschenförderung",
            "Assistência de Formação": "Ausbildungshilfe",
            "Economato Geral": "Allgemeine Wirtschaft",
            "Assistência Internacional": "Internationale Hilfe",
            "Escritório Geral": "Generalbüro",
            "Assistência Comunitária": "Gemeinschaftshilfe",
            "Assessoria Litúrgico-Sacramental": "Liturgisch-Sakramentale Beratung",
            "Assistência de Comunicação": "Kommunikationshilfe",
            "Secretaria de Tecnologia": "Technologiesekretariat",
            "Secretaria de Planejamento e Gestão": "Sekretariat für Planung und Verwaltung",
            "Assistência Local": "Lokale Hilfe",
            "Instituto Parresia": "Parresia-Institut",
            "Secretaria dos Sacerdotes e Seminaristas": "Sekretariat der Priester und Seminaristen",
            "Setor dos Celibatários": "Sektor der Unverheirateten",
            "Setor Família": "Familiensektor",
            "Secretaria de Setores Produtivos": "Sekretariat der Produktiven Sektoren"
        }
    }
}

# 5. ESTRUTURA DO BANCO (chaves em Português)
DB_STRUCTURE_PT = {
    "Assistência Missionária": [
        "Taxa de crescimento de difusões em novas dioceses",
        "Taxa de fundações em novas dioceses",
        "Percentual da abertura de novas irradiações nas missões da Comunidade (2026-2029)",
        "Evolução Média de Competência em Gestão Estratégica e Orçamentária",
        "Índice de consolidação regional",
        "IQSA (Índice de qualidade do serviço de autoridade)",
        "Taxa de Execução do PDI (Plano de Desenvolvimento Individual) dos RLs (Responsáveis Locais)",
        "Percentual de Execução do Plano de Capacitações da Assistência Missionária",
        "Índice de efetivação de novas autoridades formadas",
        "Percentual de Execução do Plano de Capacitações das lideranças (RLs, CLs, NDO)",
        "Percentual de Relação Eclesial com Bispos",
        "Percentual de Relação Eclesial com autoridades eclesiásticas devidas"
    ],
    "Assistência Apostólica": [
        "Percentual de aumento de pessoas alcançadas por meio das ações querigmáticas",
        "Número de membros no grupo de oração",
        "Taxa de permanência dos ingressantes após 6 meses na obra",
        "Percentual de pessoas acompanhadas nos Grupos de Oração",
        "Percentual de pessoas engajadas em ministérios na Obra",
        "Taxa de acolhimento de participantes nos CEVs (Centros de Evangelização) e eventos",
        "Percentual de satisfação dos participantes do evento",
        "Percentual de crescimento de novas produções artísticas (espetáculos, músicas, etc.)",
        "Taxa de reproduções das novas produções artísticas",
        "Taxa de pessoas alcançadas pelas novas produções artísticas",
        "Percentual de implantação de novas estratégias evangelizadoras",
        "Percentual de pessoas alcançadas pelas novas estratégias evangelizadoras",
        "Percentual de evangelizadores formados em inteligência evangelizadora"
    ],
    "Assessoria Jovem": [
        "Percentual de jovens na obra",
        "Índice de alcance jovem nos veículos Comshalom",
        "Índice de qualidade dos eventos para jovens",
        "Porcentagem de crescimento de participantes em eventos",
        "Quantidade de jovens em missão por ano",
        "Número de atividades querigmáticas voltadas aos pobres pelos Projetos Juventude"
    ],
    "Assessoria Vocacional": [
        "Taxa de Crescimento no Número de Ingressos na Comunidade",
        "Índice de Qualidade Vocacional (IQV)",
        "Percentual de irmãos que ingressam e permanecem até as Promessas Definitivas"
    ],
    "Assessoria de Promoção Humana": [
        "Percentual de crescimento de pessoas assistidas",
        "Percentual de crescimento de adultos reintegrados na sociedade",
        "Percentual de crianças reintegradas na sociedade",
        "Percentual de casas de Promoção Humana",
        "Percentual de missões com serviços de Promoção Humana fora do Brasil",
        "Percentual de Expedições realizadas"
    ],
    "Assistência de Formação": [
        "Percentual de crescimento na adesão das ofertas formativas presenciais",
        "Percentual de crescimento na adesão das ofertas formativas online",
        "Percentual de irmãos da Comunidade com Acompanhamento Comunitário (AC) trimestral",
        "Média ponderada da frequência de acompanhamento comunitário",
        "Percentual de irmãos que vivem os compromissos oracionais da espiritualidade Shalom",
        "Percentual de missões que aplicaram o novo modelo de atualização da vivência da CAL (Comunidade de Aliança)",
        "Porcentagem de engajamento da Comunidade de Aliança",
        "Número de missões que realizam o 'celeiro de autoridades' para a CAL",
        "Percentual de irmãos vivendo estavelmente o ordinário da Vocação como fonte de saúde integral",
        "Número percentual de cursos e formações oferecidos com temas da atualidade"
    ],
    "Economato Geral": [
        "Percentual de membros que partilham a Comunhão de Bens",
        "Percentual de economatos locais com prestação de contas regular",
        "Número de filiais com regular prática fiscal de comércio e serviço",
        "Resultado financeiro de doações em valor absoluto",
        "Resultado financeiro de benfeitores em valor absoluto",
        "Redução da dependência financeira das missões em relação aos fundos comunitários",
        "Percentual de lideranças capacitadas em criatividade e programas de ideias",
        "Número de propostas econômicas criativas apresentadas",
        "Percentual de Missões com Base Patrimonial Regularizada",
        "Percentual de imóveis classificados como bons ou excelentes em avaliação patrimonial",
        "Percentual anual de conclusão de processos patrimoniais de aquisição",
        "Percentual de participação no treinamento de planejamento orçamentário",
        "Índice de Adesão ao Planejamento Orçamentário"
    ],
    "Assistência Internacional": [
        "Percentual de valores arrecadados com projetos aprovados",
        "Número de participações em eventos eclesiais"
    ],
    "Escritório Geral": [
        "Percentual de crescimento do valor em caixa"
    ],
    "Assistência Comunitária": [
        "Percentual de pagamento do ordinário e da dívida com o Fundo de Previdência",
        "Percentual de missionários que se sentem alcançados pela comunicação interna",
        "Índice da avaliação da realização na vivência da Unidade da CAL",
        "Percentual de membros assistidos por planos de saúde",
        "Evolução crescente da nota do Índice de Qualidade de Vida Comunitária (IQVC) anual"
    ],
    "Assessoria Litúrgico-Sacramental": [
        "Porcentagem de espaços sagrados aprovados pela Comissão",
        "Índice dos espaços sagrados"
    ],
    "Assistência de Comunicação": [
        "Tempo médio de engajamento no Portal",
        "Índice de Satisfação do Serviço de Comunicação na Comunidade",
        "Índice de Treinamentos de Evangelização Digital"
    ],
    "Secretaria de Tecnologia": [
        "Percentual de processos de gestão integrados ao sistema WOP",
        "Índice de maturidade em gestão de dados e segurança digital"
    ],
    "Secretaria de Planejamento e Gestão": [
        "Índice de desempenho das secretarias de planejamento e gestão",
        "Índice de satisfação com os processos institucionais"
    ],
    "Assistência Local": [
        "Índice de avaliação geral dos CEVs"
    ],
    "Instituto Parresia": [
        "Percentual de crescimento anual de alunos ativos",
        "Etapas executadas do projeto da Faculdade",
        "Percentual de concludentes da Escola SJPII na Comunidade de Vida",
        "Percentual de membros da Comunidade de Vida com Ensino Superior"
    ],
    "Secretaria dos Sacerdotes e Seminaristas": [
        "Percentual de presença satisfatória dos padres em missões necessárias e desafiantes",
        "Qualidade da vida de oração e litúrgica no âmbito pessoal e sua contribuição comunitária",
        "Proporção de padres, diáconos e seminaristas nos níveis de situação vocacional 1 e 2"
    ],
    "Setor dos Celibatários": [
        "Número de Celibatários da CAL que estão ou já foram em missão",
        "Percentual de celibatários com situação vocacional nos níveis 1 e 2"
    ],
    "Setor Família": [
        "Percentual de casais, noivos e namorados com situação vocacional nos níveis 1 e 2",
        "Índice de Consolidação Matrimonial (vivência da unidade, deveres de estado e missão)"
    ],
    "Secretaria de Setores Produtivos": [
        "Margem de contribuição dos setores produtivos (%)",
        "Taxa de crescimento do faturamento (%)"
    ]
}

# Mapeamento de traduções para indicadores
INDICATORS_TRANSLATIONS = {
    "Português": DB_STRUCTURE_PT,
    "English": {
        "Assistência Missionária": [
            "Growth rate of diffusions in new dioceses",
            "Rate of foundations in new dioceses",
            "Percentage of opening of new radiations in the Community missions (2026-2029)",
            "Average evolution of competence in strategic and budget management",
            "Regional consolidation index",
            "IQSA (Quality index of authority service)",
            "PDI execution rate (Individual Development Plan) of RLs (Local Responsible)",
            "Percentage of execution of the missionary assistance training plan",
            "Index of effectiveness of newly trained authorities",
            "Percentage of execution of the training plan for leaders (RLs, CLs, NDO)",
            "Percentage of ecclesial relationship with bishops",
            "Percentage of ecclesial relationship with due ecclesiastical authorities"
        ],
        "Assistência Apostólica": [
            "Percentage increase of people reached through kerygmatic actions",
            "Number of members in the prayer group",
            "Retention rate of new entrants after 6 months in the community",
            "Percentage of people accompanied in prayer groups",
            "Percentage of people engaged in ministries in the community",
            "Reception rate of participants in CEVs (Evangelization Centers) and events",
            "Percentage of satisfaction of event participants",
            "Percentage growth of new artistic productions (shows, music, etc.)",
            "Reproduction rate of new artistic productions",
            "Rate of people reached by new artistic productions",
            "Percentage of implementation of new evangelization strategies",
            "Percentage of people reached by new evangelization strategies",
            "Percentage of evangelizers trained in evangelization intelligence"
        ],
        "Assessoria Jovem": [
            "Percentage of youth in the community",
            "Youth reach index in Comshalom vehicles",
            "Quality index of events for youth",
            "Percentage growth of event participants",
            "Number of young people in mission per year",
            "Number of kerygmatic activities aimed at the poor by youth projects"
        ],
        "Assessoria Vocacional": [
            "Growth rate in the number of entries into the Community",
            "Vocational Quality Index (VQI)",
            "Percentage of brothers who enter and remain until Definitive Promises"
        ],
        "Assessoria de Promoção Humana": [
            "Percentage growth of people assisted",
            "Percentage growth of adults reintegrated into society",
            "Percentage of children reintegrated into society",
            "Percentage of human promotion houses",
            "Percentage of missions with human promotion services outside Brazil",
            "Percentage of expeditions carried out"
        ],
        "Assistência de Formação": [
            "Percentage growth in adherence to in-person training offerings",
            "Percentage growth in adherence to online training offerings",
            "Percentage of community members with quarterly community accompaniment (AC)",
            "Weighted average frequency of community accompaniment",
            "Percentage of brothers who live the prayer commitments of Shalom spirituality",
            "Percentage of missions that applied the new model of updating the experience of CAL (Alliance Community)",
            "Percentage of engagement of the Alliance Community",
            "Number of missions that carry out the 'store of authorities' for CAL",
            "Percentage of brothers living stably in the ordinary of vocation as a source of integral health",
            "Percentage number of courses and training offered with current topics"
        ],
        "Economato Geral": [
            "Percentage of members who share communion of goods",
            "Percentage of local economic services with regular accounting",
            "Number of branches with regular fiscal practice of commerce and service",
            "Financial result of donations in absolute value",
            "Financial result of benefactors in absolute value",
            "Reduction of financial dependence of missions in relation to community funds",
            "Percentage of leaders trained in creativity and ideas programs",
            "Number of creative economic proposals presented",
            "Percentage of missions with regularized patrimonial base",
            "Percentage of properties classified as good or excellent in patrimonial assessment",
            "Annual percentage of completion of patrimonial acquisition processes",
            "Percentage of participation in budget planning training",
            "Index of adherence to budget planning"
        ],
        "Assistência Internacional": [
            "Percentage of funds raised with approved projects",
            "Number of participations in ecclesiastical events"
        ],
        "Escritório Geral": [
            "Percentage growth of cash value"
        ],
        "Assistência Comunitária": [
            "Percentage of payment of ordinary and debt with the pension fund",
            "Percentage of missionaries who feel reached by internal communication",
            "Index of evaluation of achievement in the experience of unit CAL",
            "Percentage of members assisted by health insurance",
            "Growing evolution of the annual quality of life index score in the community (IQVC)"
        ],
        "Assessoria Litúrgico-Sacramental": [
            "Percentage of sacred spaces approved by the commission",
            "Index of sacred spaces"
        ],
        "Assistência de Comunicação": [
            "Average time of engagement in the portal",
            "Satisfaction index of the communication service in the community",
            "Index of digital evangelization training"
        ],
        "Secretaria de Tecnologia": [
            "Percentage of management processes integrated into the WOP system",
            "Index of maturity in data management and digital security"
        ],
        "Secretaria de Planejamento e Gestão": [
            "Performance index of planning and management secretariats",
            "Satisfaction index with institutional processes"
        ],
        "Assistência Local": [
            "General evaluation index of CEVs"
        ],
        "Instituto Parresia": [
            "Percentage annual growth of active students",
            "Executed stages of the faculty project",
            "Percentage of graduates from the SJPII school in the community of life",
            "Percentage of community of life members with higher education"
        ],
        "Secretaria dos Sacerdotes e Seminaristas": [
            "Percentage of satisfactory presence of priests in necessary and challenging missions",
            "Quality of prayer and liturgical life at the personal level and its community contribution",
            "Proportion of priests, deacons and seminarians at vocational status levels 1 and 2"
        ],
        "Setor dos Celibatários": [
            "Number of celibates of the Alliance Community who are or have been on mission",
            "Percentage of celibates with vocational status at levels 1 and 2"
        ],
        "Setor Família": [
            "Percentage of couples, boyfriends and girlfriends with vocational status at levels 1 and 2",
            "Matrimonial consolidation index (experience of unity, duties of state and mission)"
        ],
        "Secretaria de Setores Produtivos": [
            "Contribution margin of productive sectors (%)",
            "Growth rate of revenue (%)"
        ]
    }
}

# CONFIGURAÇÃO DO APP
st.set_page_config(page_title="Shalom Indicators", layout="wide")

# Session state para correções
if "corrigindo_id" not in st.session_state:
    st.session_state.corrigindo_id = None
if "mostrando_historico" not in st.session_state:
    st.session_state.mostrando_historico = None

# SIDEBAR - Seleção de Idioma
sel_lang = st.sidebar.selectbox("🌍 Language / Idioma", list(TRANSLATIONS.keys()))
t = TRANSLATIONS[sel_lang]

# INTERFACE TRADUZIDA
st.title(t["title"])
st.subheader(t["subtitle"])
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    regionais_pt_keys = list(MISSOES_PT.keys())
    regionais_display = [t["regions"][regional_pt] for regional_pt in regionais_pt_keys]
    
    idx_regional = st.selectbox(t["regional_label"], range(len(regionais_display)), 
                               format_func=lambda x: regionais_display[x])
    regional_pt = regionais_pt_keys[idx_regional]

with col2:
    missoes_display = MISSOES_PT[regional_pt]
    idx_missao = st.selectbox(t["mission_label"], range(len(missoes_display)), 
                             format_func=lambda x: missoes_display[x])
    missao_pt = missoes_display[idx_missao]

with col3:
    ano = st.selectbox(t["year_label"], [2024, 2025, 2026])

col4, col5 = st.columns(2)

with col4:
    setores_pt_keys = list(DB_STRUCTURE_PT.keys())
    setores_display = [t["sectors"][setor_pt] for setor_pt in setores_pt_keys]
    
    idx_setor = st.selectbox(t["sector_label"], range(len(setores_display)), 
                             format_func=lambda x: setores_display[x])
    setor_pt = setores_pt_keys[idx_setor]

with col5:
    pass

st.markdown("---")

# ========== PAINEL DE PROGRESSO ==========
st.markdown(f"## 📊 {t['title'].replace('Portal de', 'Progresso de')} - {missao_pt}")

# Busca dados no Supabase para essa missão e setor
try:
    registros = supabase.table("historico_indicadores").select(
        "id, indicador, ano, valor, tipo_valor, confianca, versao_ativa"
    ).eq("regional", regional_pt).eq("missao", missao_pt).eq(
        "assessoria_assistencia", setor_pt
    ).eq("versao_ativa", True).execute()
    
    registros_ativos = registros.data if registros.data else []
except:
    registros_ativos = []

# Cria dicionário de preenchidos
preenchidos = {
    (r['indicador'], r['ano']): {
        'id': r['id'],
        'valor': r['valor'],
        'tipo_valor': r['tipo_valor'],
        'confianca': r['confianca']
    }
    for r in registros_ativos
}

# Calcula progresso
indicadores_setor = DB_STRUCTURE_PT[setor_pt]
total_indicadores = len(indicadores_setor)
total_esperado = total_indicadores * 3  # 3 anos (2024, 2025, 2026)

feitos_total = len(preenchidos)
percentual_geral = (feitos_total / total_esperado) * 100 if total_esperado > 0 else 0

# Mostra barra geral
st.markdown(f"**Total Geral:** {feitos_total}/{total_esperado} ({percentual_geral:.0f}%)")
st.progress(percentual_geral / 100)

# Mostra progresso por ano
col_2024, col_2025, col_2026 = st.columns(3)

for ano_ref, col_ref in [(2024, col_2024), (2025, col_2025), (2026, col_2026)]:
    with col_ref:
        feitos_ano = sum(1 for (ind, an) in preenchidos.keys() if an == ano_ref)
        percentual_ano = (feitos_ano / total_indicadores) * 100 if total_indicadores > 0 else 0
        
        status_icon = "✅" if percentual_ano == 100 else "⚠️" if percentual_ano > 0 else "❌"
        
        st.markdown(f"**{ano_ref}: {status_icon}**")
        st.markdown(f"{feitos_ano}/{total_indicadores} ({percentual_ano:.0f}%)")
        st.progress(percentual_ano / 100)

st.markdown("---")

# ========== RESUMO DE DADOS JÁ PREENCHIDOS ==========
st.markdown("## ✅ Dados Já Registrados")

if registros_ativos:
    # Cria tabela de dados
    dados_tabela = []
    for r in registros_ativos:
        tipo = r['tipo_valor']
        valor = r['valor']
        
        if tipo == "%":
            display = f"{valor}%"
        elif tipo == "$":
            display = f"${valor:,.0f}"
        else:
            display = str(valor)
        
        dados_tabela.append({
            "Indicador": r['indicador'],
            "Ano": r['ano'],
            "Valor": display,
            "Confiança": r['confianca']
        })
    
    df = pd.DataFrame(dados_tabela)
    st.dataframe(df, use_container_width=True)
    
    # Botões de correção e histórico
    st.markdown("### 🔧 Ações")
    
    for r in registros_ativos:
        col_ind, col_correct, col_hist = st.columns([2, 1, 1])
        
        with col_ind:
            st.write(f"**{r['indicador']}** ({r['ano']})")
        
        with col_correct:
            if st.button(t["btn_correct"], key=f"corr_{r['id']}"):
                st.session_state.corrigindo_id = r['id']
                st.session_state.corrigindo_indicador = r['indicador']
                st.rerun()
        
        with col_hist:
            if st.button(t["btn_history"], key=f"hist_{r['id']}"):
                st.session_state.mostrando_historico = r['id']
                st.rerun()
else:
    st.info("📭 Nenhum dado preenchido ainda para essa combinação.")

st.markdown("---")

# ========== FORMULÁRIO DE CORREÇÃO ==========
if st.session_state.corrigindo_id:
    st.markdown("### 🔧 Corrigir Indicador")
    
    try:
        registro_original = supabase.table("historico_indicadores").select(
            "*"
        ).eq("id", st.session_state.corrigindo_id).execute()
        
        if registro_original.data:
            original = registro_original.data[0]
            
            col_info, col_form = st.columns(2)
            
            with col_info:
                st.write(f"**Indicador:** {original['indicador']}")
                st.write(f"**Ano:** {original['ano']}")
                st.write(f"**Valor Anterior:** {original['valor']}")
            
            with col_form:
                novo_valor = st.number_input(
                    t["val_label"],
                    value=int(original['valor']),
                    step=1
                )
                
                motivo = st.selectbox(
                    t["conf_label"],
                    t["correction_reasons"]
                )
                
                if motivo == t["correction_reasons"][-1]:  # "Outro"
                    motivo_detalhado = st.text_input("Explicar motivo")
                else:
                    motivo_detalhado = motivo
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button(t["btn_confirm_correct"], use_container_width=True):
                    # Marca antigo como inativo
                    supabase.table("historico_indicadores").update({
                        "versao_ativa": False
                    }).eq("id", st.session_state.corrigindo_id).execute()
                    
                    # Insere novo
                    novo_registro = {
                        "regional": original['regional'],
                        "missao": original['missao'],
                        "ano": original['ano'],
                        "assessoria_assistencia": original['assessoria_assistencia'],
                        "indicador": original['indicador'],
                        "valor": int(novo_valor),
                        "tipo_valor": original['tipo_valor'],
                        "confianca": original['confianca'],
                        "idioma_preenchimento": sel_lang,
                        "versao_ativa": True,
                        "motivo_correcao": motivo_detalhado,
                        "versao_anterior_id": st.session_state.corrigindo_id,
                        "data_preenchimento": datetime.now().isoformat()
                    }
                    
                    supabase.table("historico_indicadores").insert(novo_registro).execute()
                    
                    st.success(t["msg_success_correct"])
                    st.session_state.corrigindo_id = None
                    st.rerun()
            
            with col_btn2:
                if st.button(t["btn_cancel"], use_container_width=True):
                    st.session_state.corrigindo_id = None
                    st.rerun()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

st.markdown("---")

# ========== HISTÓRICO DE VERSÕES ==========
if st.session_state.mostrando_historico:
    st.markdown("### 📋 Histórico de Versões")
    
    try:
        # Busca todas as versões
        todas_versoes = supabase.table("historico_indicadores").select(
            "*"
        ).or_rows(
            f"id.eq.{st.session_state.mostrando_historico},versao_anterior_id.eq.{st.session_state.mostrando_historico}"
        ).order("created_at", desc=True).execute()
        
        if todas_versoes.data:
            for idx, versao in enumerate(todas_versoes.data, 1):
                status = "✅ ATIVO" if versao['versao_ativa'] else "🔄 CORRIGIDO"
                motivo = f" ({versao['motivo_correcao']})" if versao.get('motivo_correcao') else ""
                
                st.write(f"**v{idx}** {status}{motivo}")
                st.caption(f"Valor: {versao['valor']} | {versao['data_preenchimento'][:10]}")
    except Exception as e:
        st.error(f"Erro ao carregar histórico: {e}")

st.markdown("---")

# ========== FORMULÁRIO PRINCIPAL ==========
st.markdown("## 📝 Preencher Novo Indicador")

if sel_lang in INDICATORS_TRANSLATIONS and setor_pt in INDICATORS_TRANSLATIONS[sel_lang]:
    indicadores_display = INDICATORS_TRANSLATIONS[sel_lang][setor_pt]
else:
    indicadores_display = DB_STRUCTURE_PT[setor_pt]

idx_ind = st.selectbox(t["indicator_label"], range(len(indicadores_display)), 
                       format_func=lambda x: indicadores_display[x])
indicador_pt = DB_STRUCTURE_PT[setor_pt][idx_ind]

# Detectar formato
formato = detect_indicator_format(indicador_pt)

# Verificar se já foi preenchido
ja_preenchido = (indicador_pt, ano) in preenchidos

if ja_preenchido:
    st.warning(t["msg_already_filled"].format(ano=ano))
    st.info(f"Valor registrado: {preenchidos[(indicador_pt, ano)]['valor']} | Confiança: {preenchidos[(indicador_pt, ano)]['confianca']}")
else:
    st.success(t["msg_pending"])

col_valor, col_confianca = st.columns(2)

with col_valor:
    if formato == "%":
        valor = st.number_input(t["val_label"] + " (0-100)", min_value=0, max_value=100, step=1)
    elif formato == "#":
        valor = st.number_input(t["val_label"] + " (inteiro)", min_value=0, step=1)
    else:  # $
        valor = st.number_input(t["val_label"] + " (inteiro)", min_value=0, step=1)

with col_confianca:
    confianca_keys = t["confidence_options"]
    confianca_pt_map = {
        "Sistema": "Sistema",
        "Planilha": "Planilha",
        "Chute/Estimativa": "Chute/Estimativa",
        "System": "Sistema",
        "Spreadsheet": "Planilha",
        "Guess/Estimate": "Chute/Estimativa",
        "Sistema": "Sistema",
        "Hoja de cálculo": "Planilha",
        "Estimación": "Chute/Estimativa",
        "Sistema": "Sistema",
        "Foglio di calcolo": "Planilha",
        "Stima": "Chute/Estimativa",
        "Système": "Sistema",
        "Feuille de calcul": "Planilha",
        "Estimation": "Chute/Estimativa",
        "System": "Sistema",
        "Tabellenkalkulation": "Planilha",
        "Schätzung": "Chute/Estimativa"
    }
    
    confianca_idx = st.selectbox(t["conf_label"], range(len(confianca_keys)), 
                                format_func=lambda x: confianca_keys[x])
    confianca_pt = confianca_pt_map.get(confianca_keys[confianca_idx], confianca_keys[confianca_idx])

if st.button(t["btn_save"], use_container_width=True, disabled=ja_preenchido):
    payload = {
        "regional": regional_pt,
        "missao": missao_pt,
        "ano": ano,
        "assessoria_assistencia": setor_pt,
        "indicador": indicador_pt,
        "valor": int(valor),
        "tipo_valor": formato,
        "confianca": confianca_pt,
        "idioma_preenchimento": sel_lang,
        "versao_ativa": True,
        "motivo_correcao": None,
        "versao_anterior_id": None,
        "data_preenchimento": datetime.now().isoformat()
    }
    try:
        supabase.table("historico_indicadores").insert(payload).execute()
        st.success(t["msg_success"])
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")

# RODAPÉ
st.markdown("---")
st.markdown("<div style='text-align: center; color: #999; font-size: 12px;'>Desenvolvido por Lume Rev Consultoria</div>", unsafe_allow_html=True)
