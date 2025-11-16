# 📊 Projeto Jurimetria - Análise Estatística de Dados Judiciais

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Sistema completo de análise jurimétrica (estatística aplicada ao direito) para dados do Poder Judiciário brasileiro, incluindo análises descritivas, preditivas, de sobrevivência e detecção de quebras estruturais.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Outputs Gerados](#outputs-gerados)
- [Docker](#docker)
- [Jupyter Notebook](#jupyter-notebook)
- [Validação e Testes](#validação-e-testes)
- [Integração com DataJud](#integração-com-datajud)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## 🎯 Visão Geral

Este projeto fornece um **pipeline completo** para análise de dados judiciais, permitindo:

- **Análise descritiva**: Estatísticas e visualizações sobre processos judiciais
- **Análise preditiva**: Modelos de machine learning para prever desfechos processuais
- **Análise de sobrevivência**: Estimativas de tempo de tramitação usando Kaplan-Meier e Cox
- **Detecção de quebras estruturais**: Identificação de mudanças em séries temporais judiciais

### Decisões de Infraestrutura

✅ **Containerização com Docker** para portabilidade e reprodutibilidade  
✅ **3 Tribunais Pilotos** simulados (TJ-SP, TJ-RJ, TJ-MG)  
✅ **Múltiplos formatos de output**: CSV, JSON, HTML, PNG  
✅ **Estrutura pronta para integração com DataJud API**  

## ✨ Funcionalidades

### 1. Análise Descritiva
- Estatísticas descritivas completas
- Distribuição temporal de processos
- Análise por tribunal, juiz e classe processual
- Visualizações: histogramas, boxplots, gráficos de barras

### 2. Análise Preditiva
- Regressão logística para prever desfechos processuais
- Cross-validation (5-fold)
- Cálculo de Odds Ratios
- Matriz de confusão e métricas de classificação

### 3. Análise de Sobrevivência
- Curvas Kaplan-Meier por classe processual
- Teste Log-Rank para comparação entre grupos
- Modelo Cox de Riscos Proporcionais
- Hazard Ratios para fatores de risco

### 4. Detecção de Quebras Estruturais
- Análise de séries temporais
- Identificação de pontos de mudança significativa

## 🛠️ Requisitos

- **Python**: 3.8 ou superior
- **Docker**: (opcional) para execução containerizada
- **Sistema Operacional**: Linux, macOS ou Windows

### Dependências Python

As principais bibliotecas utilizadas:

```
pandas >= 2.0.0
numpy >= 1.24.0
scikit-learn >= 1.3.0
matplotlib >= 3.7.0
seaborn >= 0.12.0
lifelines >= 0.27.0
jupyter >= 1.0.0
```

Veja a lista completa em `requirements.txt`.

## 📦 Instalação

### Opção 1: Instalação Local (Python)

```bash
# Clone o repositório
git clone https://github.com/Joicerss/projeto-novo.git
cd projeto-novo

# Crie um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### Opção 2: Instalação com Docker

```bash
# Clone o repositório
git clone https://github.com/Joicerss/projeto-novo.git
cd projeto-novo

# Build da imagem
docker-compose build
```

## 🚀 Uso

### Execução Local

```bash
# Executar análise completa
python3 jurimetria_completa.py

# Os resultados serão salvos em ./output/
```

### Execução com Docker

```bash
# Executar análise completa
docker-compose up jurimetria

# Executar Jupyter Notebook
docker-compose --profile jupyter up jupyter
# Acesse: http://localhost:8888
```

### Usando seus próprios dados

Para usar dados reais ao invés dos simulados:

1. Prepare seus dados no formato CSV com as colunas esperadas
2. Salve em `data/dados_reais.csv`
3. Modifique a função `main()` em `jurimetria_completa.py` para carregar seus dados:

```python
# Substituir esta linha:
df = gerar_dados_simulados(n_processos=150)

# Por esta:
df = pd.read_csv(DATA_DIR / 'dados_reais.csv')
```

## 📁 Estrutura do Projeto

```
projeto-novo/
├── README.md                          # Este arquivo
├── requirements.txt                   # Dependências Python
├── Dockerfile                         # Configuração Docker
├── docker-compose.yml                 # Orquestração de containers
├── jurimetria_completa.py            # Script principal de análise
├── generate_report_complete.py       # Gerador de relatórios HTML
├── validacao_dados.py                # Script de validação de dados
├── test_jurimetria.py                # Testes automatizados
├── .gitignore                        # Arquivos ignorados pelo Git
│
├── data/                             # Dados de entrada
│   ├── template_dados.xlsx           # Planilha modelo
│   └── dados_simulados.csv           # Dados gerados (exemplo)
│
├── output/                           # Resultados das análises
│   ├── *.png                         # Visualizações
│   ├── *.csv                         # Tabelas de resultados
│   ├── *.json                        # Relatórios JSON
│   └── report_complete.html          # Relatório HTML completo
│
├── notebooks/                        # Jupyter notebooks
│   └── exemplo_workflow.ipynb        # Notebook de exemplo
│
└── docs/                            # Documentação adicional
    └── integracao_datajud.md        # Guia de integração DataJud
```

## 📊 Outputs Gerados

Após executar a análise, os seguintes arquivos são gerados em `output/`:

### Visualizações (PNG)
- `distribuicao_tempo_tramitacao.png` - Histograma do tempo de tramitação
- `resultado_por_juiz.png` - Contagem de resultados por juiz
- `boxplot_valor_causa.png` - Boxplot do valor da causa por resultado
- `kaplan_meier_survival.png` - Curva de sobrevivência Kaplan-Meier
- `quebra_estrutural_detectada.png` - Detecção de quebra estrutural

### Tabelas (CSV)
- `resultados_regressao_logistica.csv` - Odds ratios do modelo
- `hazard_ratios_cox.csv` - Hazard ratios do modelo Cox
- `classification_report.txt` - Relatório de classificação
- `confusion_matrix.csv` - Matriz de confusão
- `cv_scores.csv` - Scores de cross-validation

### Relatórios
- `report_complete.html` - Relatório HTML completo com todas as visualizações
- `relatorio_estatisticas.json` - Estatísticas em formato JSON

## 🐳 Docker

### Comandos Úteis

```bash
# Build da imagem
docker-compose build

# Executar análise
docker-compose up jurimetria

# Executar em background
docker-compose up -d jurimetria

# Ver logs
docker-compose logs -f jurimetria

# Parar containers
docker-compose down

# Executar Jupyter
docker-compose --profile jupyter up jupyter
```

### Executar comando customizado

```bash
docker-compose run jurimetria python3 -c "print('Hello from container')"
```

## 📓 Jupyter Notebook

O projeto inclui notebooks interativos para exploração e demonstração:

### Iniciar Jupyter

```bash
# Local
jupyter notebook

# Docker
docker-compose --profile jupyter up jupyter
```

### Notebooks Disponíveis

- `exemplo_workflow.ipynb` - Workflow completo passo a passo
- (adicione mais notebooks conforme necessário)

## ✅ Validação e Testes

### Validação de Dados

Execute o script de validação para verificar a qualidade dos dados:

```bash
python3 validacao_dados.py
```

### Testes Automatizados

Execute os testes unitários:

```bash
# Instalar pytest (se ainda não tiver)
pip install pytest pytest-cov

# Executar testes
pytest test_jurimetria.py -v

# Executar com cobertura
pytest test_jurimetria.py --cov=. --cov-report=html
```

## 🔌 Integração com DataJud

O projeto está estruturado para facilitar a integração com a API do DataJud (CNJ).

### Estrutura Preparada

O código já possui:
- Funções modulares para carregar dados
- Suporte a múltiplas fontes de dados
- Validação de esquema de dados

### Para integrar com DataJud:

1. Obtenha as credenciais de API do DataJud/CNJ
2. Configure as variáveis de ambiente:
   ```bash
   export DATAJUD_API_KEY="sua-chave-aqui"
   export DATAJUD_API_URL="https://api.datajud.cnj.jus.br"
   ```
3. Implemente a função de coleta (exemplo em `docs/integracao_datajud.md`)

**Nota**: Este MVP usa dados simulados para demonstração. A integração real com DataJud requer credenciais e conformidade com a LGPD.

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes

- Mantenha o código limpo e documentado
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Siga as boas práticas de código Python (PEP 8)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Projeto Jurimetria** - Desenvolvimento inicial

## 📞 Suporte

Para questões e suporte:

- Abra uma [Issue](https://github.com/Joicerss/projeto-novo/issues)
- Entre em contato via email (configure conforme necessário)

## 🙏 Agradecimentos

- CNJ (Conselho Nacional de Justiça) pela iniciativa DataJud
- Comunidade de desenvolvedores Python e Data Science
- Contribuidores do projeto

---

**Nota**: Os dados usados neste projeto são simulados para fins de demonstração. Ao trabalhar com dados reais do Poder Judiciário, certifique-se de seguir todas as diretrizes de privacidade e conformidade com a LGPD.
