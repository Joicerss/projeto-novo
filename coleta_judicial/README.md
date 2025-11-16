# Coletor Automatizado de Dados Judiciais

Sistema automatizado para coleta de dados de processos judiciais de recuperação judicial envolvendo o banco Itaú e empresas do setor de veículos pesados nos Tribunais de Justiça brasileiros.

## 📋 Descrição

Este projeto automatiza a coleta de dados de processos judiciais para responder questões específicas sobre recuperação judicial no setor de veículos pesados, incluindo:

1. Principais motivos que levam empresas do setor a entrarem em recuperação judicial
2. Taxa de sucesso das recuperações judiciais neste setor
3. Tempo médio de tramitação dos processos
4. Garantias mais comumente oferecidas
5. Papel dos bancos (especialmente Itaú) nesses processos
6. Principais credores além dos bancos
7. Padrões regionais ou temporais nos pedidos de recuperação

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação das dependências

```bash
# No diretório raiz do projeto
pip install -r requirements.txt
```

### Dependências opcionais

Para recursos avançados de scraping (se necessário):

```bash
# Instalar Playwright (navegador headless)
playwright install chromium

# Para OCR (se processos tiverem PDFs escaneados)
# pip install pytesseract Pillow
# E instalar Tesseract-OCR no sistema
```

## 📁 Estrutura do Projeto

```
coleta_judicial/
│
├── __init__.py              # Inicialização do pacote
├── config.py                # Configurações (bancos, tribunais, datas)
├── base_scraper.py          # Classe base para scrapers
├── tjsp_scraper.py          # Scraper específico para TJSP
├── data_exporter.py         # Exportação de dados (CSV, JSON, Excel)
├── main_collector.py        # Script principal de orquestração
└── README.md                # Esta documentação

resultados_coleta/           # Diretório criado automaticamente
├── processos_YYYYMMDD_HHMMSS.csv
├── processos_YYYYMMDD_HHMMSS.json
└── resumo_coleta.txt
```

## 🔧 Configuração

Edite o arquivo `config.py` para personalizar:

- **BANKS**: Lista de bancos a buscar (padrão: Itaú)
- **KEYWORDS**: Palavras-chave de busca (recuperação judicial, veículos pesados, etc.)
- **TRIBUNALS**: Tribunais a consultar (TJSP configurado, outros podem ser adicionados)
- **DATE_START/DATE_END**: Período de busca
- **OUTPUT_FORMAT**: Formato de saída (csv, json, xlsx)

## 🏃 Uso

### Execução básica

```bash
cd coleta_judicial
python main_collector.py
```

### Execução programática

```python
from coleta_judicial import JudicialDataCollector

collector = JudicialDataCollector()
collector.run()
```

### Uso individual de componentes

```python
# Usar apenas o scraper do TJSP
from coleta_judicial import TJSPScraper

scraper = TJSPScraper(
    search_url="https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do",
    timeout=30
)

results = scraper.search_processes(
    keywords=["recuperação judicial", "Itaú"],
    date_start="01/01/2023",
    date_end="31/12/2025"
)

# Exportar resultados
from coleta_judicial import DataExporter

exporter = DataExporter(output_dir="meus_resultados")
exporter.export_to_csv(results, "processos_tjsp.csv")
```

## 📊 Formatos de Saída

### CSV
Formato tabular simples, ideal para análise em Excel ou ferramentas estatísticas.

### JSON
Formato estruturado completo, preserva hierarquias (partes, movimentações).

### Excel (XLSX)
Formato formatado com colunas ajustadas automaticamente.

## ⚙️ Funcionalidades

### Implementadas

- ✅ Estrutura base de scraping com retry e timeout
- ✅ Configuração centralizada e flexível
- ✅ Scraper template para TJSP
- ✅ Exportação em múltiplos formatos (CSV, JSON, Excel)
- ✅ Logging detalhado de operações
- ✅ Tratamento de erros robusto
- ✅ Sistema modular e extensível

### A implementar (requer análise da estrutura real dos sites)

- ⏳ Implementação completa da lógica de busca no TJSP
- ⏳ Parser de HTML específico para TJSP
- ⏳ Scrapers para outros tribunais (TJRJ, TJMG, etc.)
- ⏳ Tratamento de CAPTCHA
- ⏳ Navegação de paginação
- ⏳ Extração de PDFs e anexos
- ⏳ Cache de resultados

## 🔍 Observações Importantes

### Aspectos Legais e Éticos

1. **Respeite o robots.txt**: Verifique as políticas de acesso de cada tribunal
2. **Rate limiting**: O sistema inclui delays entre requisições
3. **Dados públicos**: Colete apenas dados públicos disponíveis
4. **LGPD**: Ao lidar com dados pessoais, siga a Lei Geral de Proteção de Dados
5. **Uso responsável**: Não sobrecarregue os servidores dos tribunais

### Limitações Técnicas

1. **CAPTCHAs**: Muitos tribunais usam CAPTCHA - pode requerer intervenção manual ou serviços de resolução
2. **JavaScript dinâmico**: Alguns sites requerem Playwright/Selenium em vez de requests simples
3. **Estrutura HTML**: A estrutura dos sites pode mudar, requerendo atualização dos parsers
4. **Acesso restrito**: Alguns dados podem requerer login/certificado digital

## 🛠️ Desenvolvimento

### Adicionar novo tribunal

1. Crie um novo arquivo `tj[SIGLA]_scraper.py`
2. Herde de `BaseJudicialScraper`
3. Implemente os métodos `search_processes` e `extract_process_info`
4. Adicione configuração em `config.py`

Exemplo:

```python
from base_scraper import BaseJudicialScraper

class TJRJScraper(BaseJudicialScraper):
    def __init__(self, search_url, timeout=30):
        super().__init__('TJRJ', 'http://www4.tjrj.jus.br', timeout)
        self.search_url = search_url
    
    def search_processes(self, keywords, date_start, date_end):
        # Implementar lógica específica do TJRJ
        pass
```

### Executar testes

```bash
# Testar módulos individualmente
python -m coleta_judicial.base_scraper
python -m coleta_judicial.data_exporter

# Executar com dados de teste
python main_collector.py --test-mode
```

## 📝 Logs

Os logs são salvos em:
- Console (stdout)
- Arquivo `coleta_judicial.log`

Níveis de log:
- INFO: Operações normais
- WARNING: Avisos e situações incomuns
- ERROR: Erros que não impedem a execução completa
- CRITICAL: Erros graves

## 🤝 Contribuindo

Contribuições são bem-vindas! Áreas prioritárias:

1. Implementação completa dos parsers de tribunais
2. Tratamento de CAPTCHAs
3. Scrapers para tribunais adicionais
4. Testes automatizados
5. Documentação adicional

## 📄 Licença

Este projeto é desenvolvido para fins acadêmicos e de pesquisa em jurimetria.

## 📞 Suporte

Para questões ou problemas:
1. Verifique os logs em `coleta_judicial.log`
2. Consulte a documentação dos tribunais
3. Abra uma issue no repositório

## 🔄 Próximas Etapas

1. **Análise dos sites**: Inspecionar HTML real do TJSP e outros tribunais
2. **Implementação dos parsers**: Desenvolver lógica específica de extração
3. **Testes**: Validar com buscas reais
4. **Expansão**: Adicionar mais tribunais
5. **Análise de dados**: Processar dados coletados para responder as questões de pesquisa

---

**Nota**: Este é um sistema template. A implementação completa requer:
- Análise detalhada da estrutura HTML de cada tribunal
- Testes com dados reais
- Possível uso de Selenium/Playwright para sites dinâmicos
- Tratamento de autenticação e CAPTCHAs conforme necessário
