# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-11-16

### Adicionado
- Script principal de análise jurimétrica (`jurimetria_completa.py`)
  - Análise descritiva completa
  - Análise preditiva com regressão logística
  - Análise de sobrevivência (Kaplan-Meier e Cox)
  - Detecção de quebras estruturais
  - Geração de relatórios JSON e HTML
  
- Script de validação de dados (`validacao_dados.py`)
  - Validação de colunas obrigatórias
  - Verificação de valores nulos
  - Detecção de duplicatas
  - Validação de valores numéricos e categóricos
  - Verificação de consistência temporal
  
- Suite de testes automatizados (`test_jurimetria.py`)
  - 24 testes unitários cobrindo funcionalidades principais
  - Testes de geração de dados
  - Testes de validação
  - Testes de análises descritivas e comparativas
  - Testes de integridade e robustez
  
- Infraestrutura Docker
  - `Dockerfile` para containerização
  - `docker-compose.yml` para orquestração
  - Suporte a Jupyter Notebook via Docker
  
- Documentação completa
  - README.md em português com instruções detalhadas
  - Guia de integração com DataJud (`docs/integracao_datajud.md`)
  - Estrutura de projeto bem documentada
  
- Jupyter Notebook interativo
  - `notebooks/exemplo_workflow.ipynb`
  - Workflow completo com exemplos
  - Visualizações interativas
  
- Template de dados
  - Planilha Excel modelo (`data/template_dados.xlsx`)
  - Três abas: Dados, Instruções, Valores Válidos
  - Script gerador de template (`criar_template.py`)
  
- Scripts auxiliares
  - `quick_start.sh` - Script de início rápido
  - `generate_report_complete.py` - Gerador de relatórios HTML
  
- Configurações
  - `requirements.txt` com todas as dependências
  - `.gitignore` configurado para Python/Data Science
  - `.env.example` com template de variáveis de ambiente
  - `LICENSE` (MIT)

### Decisões de Design
- **3 Tribunais Pilotos**: TJ-SP, TJ-RJ, TJ-MG
- **Dados Simulados**: Para demonstração e testes
- **Estrutura Modular**: Fácil integração com dados reais
- **Múltiplos Formatos de Output**: CSV, JSON, HTML, PNG
- **Containerização**: Para reprodutibilidade e portabilidade

### Métricas
- 24 testes automatizados (100% passing)
- 12 visualizações geradas
- 5+ formatos de output suportados
- Documentação completa em português

## [Não Lançado]

### Planejado
- Integração real com API DataJud
- Dashboard interativo com Plotly/Dash
- Suporte a mais tipos de análises estatísticas
- API REST para consultas
- Exportação para PDF
- Suporte a múltiplos idiomas
- Integração com CI/CD
- Testes de integração
- Documentação de API
- Exemplos de casos de uso reais

---

Para mais detalhes sobre cada versão, consulte as [releases do GitHub](https://github.com/Joicerss/projeto-novo/releases).
