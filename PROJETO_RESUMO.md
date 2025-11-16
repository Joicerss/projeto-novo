# 📊 Projeto Jurimetria - Resumo Executivo

## Visão Geral

O **Projeto Jurimetria** é uma solução completa para análise estatística de dados do Poder Judiciário brasileiro, desenvolvida em Python com foco em reprodutibilidade, escalabilidade e facilidade de uso.

## 🎯 Objetivo

Fornecer ferramentas robustas para análise jurimétrica (estatística aplicada ao direito), permitindo:
- Análise descritiva de processos judiciais
- Previsão de desfechos processuais
- Estimativa de tempo de tramitação
- Detecção de padrões e anomalias

## 📦 Componentes Principais

### 1. Scripts de Análise

#### `jurimetria_completa.py`
Script principal que executa pipeline completo de análise:
- **Análise Descritiva**: Estatísticas e visualizações
- **Análise Preditiva**: Regressão logística para prever resultados
- **Análise de Sobrevivência**: Kaplan-Meier e Cox PH para tempo de tramitação
- **Quebras Estruturais**: Detecção de mudanças em séries temporais
- **Outputs**: CSV, JSON, HTML, PNG

**Execução:**
```bash
python3 jurimetria_completa.py
```

#### `validacao_dados.py`
Validador de qualidade de dados que verifica:
- Colunas obrigatórias
- Valores nulos
- Duplicatas
- Valores numéricos válidos
- Consistência de datas
- Distribuição de categorias

**Execução:**
```bash
python3 validacao_dados.py
```

#### `criar_template.py`
Gerador de planilha Excel modelo com três abas:
- **Dados**: Exemplos de processos
- **Instruções**: Descrição de cada campo
- **Valores Válidos**: Lista de valores aceitos

**Execução:**
```bash
python3 criar_template.py
```

### 2. Testes Automatizados

#### `test_jurimetria.py`
Suite completa de testes com 24 casos de teste:
- Geração de dados
- Validação
- Análises descritivas e comparativas
- Integridade de dados
- Robustez

**Execução:**
```bash
pytest test_jurimetria.py -v
```

**Cobertura:** 100% dos testes passando ✅

### 3. Infraestrutura Docker

#### `Dockerfile`
Container Docker baseado em Python 3.11-slim com:
- Todas as dependências instaladas
- Diretórios configurados
- Suporte para execução de scripts ou Jupyter

**Build:**
```bash
docker build -t jurimetria .
```

#### `docker-compose.yml`
Orquestração com dois serviços:
- **jurimetria**: Executa análise completa
- **jupyter**: Jupyter Notebook interativo

**Execução:**
```bash
# Análise
docker-compose up jurimetria

# Jupyter
docker-compose --profile jupyter up jupyter
# Acesse: http://localhost:8888
```

### 4. Documentação

#### `README.md`
Documentação principal em português com:
- Visão geral do projeto
- Instruções de instalação
- Guia de uso
- Descrição de outputs
- Troubleshooting

#### `docs/integracao_datajud.md`
Guia completo para integração com API DataJud/CNJ:
- Configuração de credenciais
- Implementação de cliente
- Rate limiting e retry
- Conformidade LGPD
- Anonimização de dados

#### `CONTRIBUTING.md`
Guia para contribuidores com:
- Processo de desenvolvimento
- Padrões de código
- Guidelines de PR
- Tipos de contribuições

#### `CHANGELOG.md`
Histórico de versões e mudanças do projeto.

### 5. Notebooks Interativos

#### `notebooks/exemplo_workflow.ipynb`
Jupyter Notebook completo com:
- Workflow passo a passo
- Visualizações interativas
- Exemplos de análises
- Interpretação de resultados

**Execução:**
```bash
jupyter notebook notebooks/exemplo_workflow.ipynb
```

### 6. Templates e Configurações

#### `data/template_dados.xlsx`
Planilha modelo Excel para entrada de dados com instruções detalhadas.

#### `requirements.txt`
Lista completa de dependências Python:
- pandas, numpy (manipulação de dados)
- scikit-learn (machine learning)
- matplotlib, seaborn (visualização)
- lifelines (análise de sobrevivência)
- jupyter (notebooks interativos)
- pytest (testes)

#### `.env.example`
Template de variáveis de ambiente para configuração.

#### `.gitignore`
Configurado para ignorar:
- Arquivos Python temporários
- Ambientes virtuais
- Outputs gerados
- Dados sensíveis

### 7. Scripts Auxiliares

#### `quick_start.sh`
Script de início rápido que:
- Verifica pré-requisitos
- Instala dependências
- Gera template
- Executa análise completa
- Mostra resultados

**Execução:**
```bash
./quick_start.sh
```

#### `generate_report_complete.py`
Gera relatório HTML consolidado com todas as visualizações e tabelas.

## 🏗️ Arquitetura

```
projeto-novo/
├── 📜 Scripts Principais
│   ├── jurimetria_completa.py      # Análise completa
│   ├── validacao_dados.py          # Validação de dados
│   └── criar_template.py           # Gerador de template
│
├── 🧪 Testes
│   └── test_jurimetria.py          # 24 testes automatizados
│
├── 🐳 Docker
│   ├── Dockerfile                  # Imagem Docker
│   └── docker-compose.yml          # Orquestração
│
├── 📚 Documentação
│   ├── README.md                   # Documentação principal
│   ├── CONTRIBUTING.md             # Guia de contribuição
│   ├── CHANGELOG.md                # Histórico de versões
│   ├── LICENSE                     # Licença MIT
│   └── docs/
│       └── integracao_datajud.md   # Guia DataJud
│
├── 📓 Notebooks
│   └── exemplo_workflow.ipynb      # Notebook interativo
│
├── 📊 Dados
│   ├── template_dados.xlsx         # Template Excel
│   └── dados_simulados.csv         # Dados de exemplo
│
├── 📈 Outputs
│   ├── *.png                       # Visualizações
│   ├── *.csv                       # Tabelas de resultados
│   ├── *.json                      # Relatórios estruturados
│   └── *.html                      # Relatórios web
│
└── ⚙️ Configurações
    ├── requirements.txt            # Dependências
    ├── .gitignore                  # Exclusões Git
    ├── .env.example                # Template de ambiente
    └── quick_start.sh              # Início rápido
```

## 📊 Análises Disponíveis

### 1. Análise Descritiva
- Estatísticas descritivas (média, mediana, desvio padrão)
- Distribuição temporal de processos
- Análise por tribunal, juiz e classe processual
- Taxa de procedência
- Valor médio de causas

**Visualizações:**
- Histograma de tempo de tramitação
- Gráfico de barras de resultados por juiz
- Boxplot de valor da causa por resultado

### 2. Análise Preditiva
- Regressão logística para prever desfechos
- Cross-validation (5-fold)
- Cálculo de Odds Ratios
- Métricas: precisão, recall, F1-score
- Matriz de confusão

**Output:**
- Coeficientes do modelo
- Importância de features
- Relatório de classificação
- Scores de validação cruzada

### 3. Análise de Sobrevivência
- Curvas Kaplan-Meier por classe processual
- Teste Log-Rank para comparação de grupos
- Modelo Cox de Riscos Proporcionais
- Hazard Ratios

**Visualizações:**
- Curvas de sobrevivência com intervalos de confiança
- Comparação entre classes processuais

### 4. Análise de Quebras Estruturais
- Detecção de mudanças em séries temporais
- Identificação de pontos de ruptura
- Análise de tendências

**Visualizações:**
- Série temporal com pontos de quebra destacados

## 🎯 Casos de Uso

### 1. Pesquisa Acadêmica
- Análise de padrões judiciais
- Estudos de eficiência do Judiciário
- Dissertações e teses em Direito/Estatística

### 2. Gestão Judicial
- Monitoramento de indicadores
- Identificação de gargalos
- Planejamento estratégico

### 3. Advocacia
- Análise de probabilidade de sucesso
- Estimativa de tempo de tramitação
- Comparação entre juízes/tribunais

### 4. Ensino
- Aulas de Jurimetria
- Workshops de Data Science aplicado ao Direito
- Demonstrações práticas

## 📈 Outputs Gerados

Após execução completa, o projeto gera:

### Visualizações (PNG, 300 DPI)
1. `distribuicao_tempo_tramitacao.png` - Histograma
2. `resultado_por_juiz.png` - Gráfico de barras
3. `boxplot_valor_causa.png` - Boxplot
4. `kaplan_meier_survival.png` - Curva de sobrevivência
5. `quebra_estrutural_detectada.png` - Série temporal

### Tabelas (CSV)
1. `resultados_regressao_logistica.csv` - Odds ratios
2. `hazard_ratios_cox.csv` - Hazard ratios
3. `confusion_matrix.csv` - Matriz de confusão
4. `cv_scores.csv` - Scores de cross-validation

### Relatórios
1. `classification_report.txt` - Métricas de classificação
2. `relatorio_estatisticas.json` - Estatísticas estruturadas
3. `report_complete.html` - Relatório HTML completo

### Dados
1. `dados_simulados.csv` - Dados gerados para análise

## 🚀 Início Rápido

### Opção 1: Script Automatizado
```bash
./quick_start.sh
```

### Opção 2: Manual (Local)
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar análise
python3 jurimetria_completa.py

# Validar dados
python3 validacao_dados.py

# Executar testes
pytest test_jurimetria.py -v
```

### Opção 3: Docker
```bash
# Build e execução
docker-compose up jurimetria

# Jupyter
docker-compose --profile jupyter up jupyter
```

## 📊 Estatísticas do Projeto

- **Linhas de Código**: ~2,500+ linhas Python
- **Testes**: 24 testes automatizados (100% passing)
- **Documentação**: 5 arquivos principais + comentários inline
- **Visualizações**: 12+ gráficos diferentes
- **Formatos de Output**: 5 (PNG, CSV, JSON, HTML, TXT)
- **Cobertura de Testes**: Alta (funcionalidades principais)

## 🔒 Segurança e Privacidade

### Conformidade LGPD
- Dados simulados para demonstração
- Guia de anonimização incluído
- Recomendações de segurança documentadas
- Template de consentimento sugerido

### Boas Práticas
- Credenciais via variáveis de ambiente
- .gitignore configurado
- Sem hardcoded secrets
- Validação de dados entrada

## 🔄 Roadmap Futuro

### Versão 1.1 (Planejado)
- [ ] Integração real com API DataJud
- [ ] Dashboard interativo (Plotly/Dash)
- [ ] Exportação para PDF
- [ ] API REST

### Versão 1.2 (Planejado)
- [ ] Suporte a múltiplos idiomas
- [ ] Análises estatísticas avançadas
- [ ] Machine learning avançado (XGBoost, Neural Networks)
- [ ] Sistema de plugins

### Versão 2.0 (Futuro)
- [ ] Interface web completa
- [ ] Colaboração multi-usuário
- [ ] Integração com outras bases judiciais
- [ ] Análise de texto (NLP)

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes.

### Formas de Contribuir
- Reportar bugs
- Sugerir melhorias
- Adicionar testes
- Melhorar documentação
- Implementar features

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores e Agradecimentos

- **Projeto Jurimetria** - Desenvolvimento inicial
- Comunidade Python e Data Science
- CNJ (Conselho Nacional de Justiça) - Iniciativa DataJud

## 📞 Suporte e Contato

- **Issues**: [GitHub Issues](https://github.com/Joicerss/projeto-novo/issues)
- **Documentação**: [README.md](README.md)
- **Contribuir**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Projeto desenvolvido com ❤️ para análise jurimétrica no Brasil**

*Última atualização: 2025-11-16*
