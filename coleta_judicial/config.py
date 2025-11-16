"""
Configuration file for judicial data collection
Edit this file to customize search parameters
"""

# Banks to search for (add more as needed)
BANKS = [
    "Itaú",
    "Banco Itaú",
    "Itaú Unibanco",
]

# Keywords for search
KEYWORDS = [
    "recuperação judicial",
    "veículos pesados",
    "caminhões",
    "ônibus",
]

# Court systems (Tribunais de Justiça)
TRIBUNALS = {
    "TJSP": {
        "name": "Tribunal de Justiça de São Paulo",
        "base_url": "https://esaj.tjsp.jus.br",
        "search_url": "https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do",
    },
    # Add more tribunals as needed
    # "TJRJ": {
    #     "name": "Tribunal de Justiça do Rio de Janeiro",
    #     "base_url": "http://www4.tjrj.jus.br",
    #     "search_url": "http://www4.tjrj.jus.br/consultaProcessoWebV2/consultaProc.do",
    # },
}

# Date range for search (format: DD/MM/YYYY)
DATE_START = "01/01/2023"
DATE_END = "31/12/2025"

# Output settings
OUTPUT_FORMAT = "csv"  # Options: csv, json, xlsx
OUTPUT_DIR = "resultados_coleta"

# Scraping settings
TIMEOUT = 30  # seconds
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = 2  # seconds

# Questions to answer (for documentation purposes)
RESEARCH_QUESTIONS = [
    "1. Quais são os principais motivos que levam empresas do setor de veículos pesados a entrarem em recuperação judicial?",
    "2. Qual é a taxa de sucesso das recuperações judiciais neste setor?",
    "3. Qual o tempo médio de tramitação desses processos?",
    "4. Quais são as garantias mais comumente oferecidas?",
    "5. Qual o papel dos bancos (especialmente Itaú) nesses processos?",
    "6. Quais são os principais credores além dos bancos?",
    "7. Há padrões regionais ou temporais nos pedidos de recuperação?",
]
