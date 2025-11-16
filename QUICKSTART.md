# Guia de Início Rápido - Sistema de Coleta de Dados Judiciais

## ⚡ Quick Start

### 1. Clone e Navegue

```bash
cd projeto-novo
```

### 2. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 3. Configure os Parâmetros

Edite `coleta_judicial/config.py` conforme necessário:

```python
# Bancos a buscar
BANKS = ["Itaú", "Banco Itaú", "Itaú Unibanco"]

# Palavras-chave
KEYWORDS = ["recuperação judicial", "veículos pesados", "caminhões"]

# Período de busca
DATE_START = "01/01/2023"
DATE_END = "31/12/2025"

# Formato de saída
OUTPUT_FORMAT = "csv"  # ou "json", "xlsx"
```

### 4. Execute a Coleta

**Opção A - Execução Completa:**
```bash
cd coleta_judicial
python main_collector.py
```

**Opção B - Exemplos Interativos:**
```bash
cd coleta_judicial
python examples.py
```

**Opção C - Uso Programático:**
```python
from coleta_judicial import JudicialDataCollector

collector = JudicialDataCollector()
collector.run()
```

## 📂 Onde Encontrar os Resultados

Os dados coletados serão salvos em:
```
resultados_coleta/
├── processos_YYYYMMDD_HHMMSS.csv
├── processos_YYYYMMDD_HHMMSS.json
└── resumo_coleta.txt
```

## 🔍 Verificar a Instalação

Execute o teste de estrutura:
```bash
python test_structure.py
```

Você deve ver:
```
✓ All basic structure tests passed!
```

## 📖 Documentação Completa

- **Sistema de Coleta**: [coleta_judicial/README.md](coleta_judicial/README.md)
- **Projeto Principal**: [README.md](README.md)

## 🎯 Questões que o Sistema Busca Responder

1. Principais motivos de recuperação judicial no setor de veículos pesados
2. Taxa de sucesso das recuperações judiciais
3. Tempo médio de tramitação
4. Garantias oferecidas
5. Papel do Itaú nos processos
6. Principais credores
7. Padrões regionais/temporais

## ⚠️ Nota Importante

Este sistema fornece um **template funcional** para coleta de dados. Para uso em produção:

1. **Inspecione o HTML real** dos sites dos tribunais
2. **Implemente a lógica de parsing** específica em `tjsp_scraper.py`
3. **Teste com buscas reais** e ajuste conforme necessário
4. **Trate CAPTCHAs** se necessário
5. **Respeite robots.txt** e políticas de uso

## 🚨 Limitações Conhecidas

- ⚠️ Parsing HTML requer implementação específica para cada tribunal
- ⚠️ Alguns sites podem requerer Selenium/Playwright para JavaScript
- ⚠️ CAPTCHAs podem impedir automação completa
- ⚠️ Rate limiting pode ser necessário
- ⚠️ Alguns dados podem requerer autenticação

## 🆘 Precisa de Ajuda?

1. Verifique os logs: `coleta_judicial/coleta_judicial.log`
2. Consulte a documentação: `coleta_judicial/README.md`
3. Execute os exemplos: `python examples.py`
4. Verifique a estrutura: `python test_structure.py`

## 🔄 Próximos Passos

1. ✅ Sistema estruturado e modular
2. ✅ Configuração centralizada
3. ✅ Documentação completa
4. ⏳ Implementar parsing HTML específico
5. ⏳ Testar com dados reais
6. ⏳ Adicionar mais tribunais
7. ⏳ Implementar análise dos dados coletados

---

**Pronto para começar?** Execute:
```bash
python test_structure.py && cd coleta_judicial && python examples.py
```
