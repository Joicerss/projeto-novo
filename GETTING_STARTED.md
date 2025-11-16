# Guia de Início Rápido - Projeto Jurimetria

## 🚀 Começando

Este guia vai te ajudar a configurar e entender o projeto passo a passo.

## 📋 Pré-requisitos

### Opção 1: Usando Python
```bash
# Python 3.8 ou superior
python --version

# pip (gerenciador de pacotes Python)
pip --version
```

### Opção 2: Usando R
```bash
# R instalado
R --version

# RStudio (opcional, mas recomendado)
```

## 🔧 Configuração do Ambiente

### Passo 1: Clone o Repositório

Se você ainda não tem o projeto localmente:

```bash
git clone https://github.com/Joicerss/projeto-novo.git
cd projeto-novo
```

### Passo 2: Instale as Dependências Python

Crie um arquivo `requirements.txt` com as dependências necessárias:

```bash
# Crie o arquivo (será criado automaticamente no próximo passo da documentação)
cat > requirements.txt << EOF
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
scikit-learn>=0.24.0
lifelines>=0.27.0
scipy>=1.7.0
EOF

# Instale as dependências
pip install -r requirements.txt
```

## 📊 Explorando os Resultados Existentes

O projeto já contém resultados de análises prontos. Vamos explorá-los:

### 1. Visualize as Imagens

Abra as imagens PNG no seu navegador ou visualizador de imagens:

```bash
# No Windows
start distribuicao_tempo_tramitacao.png
start resultado_por_juiz.png
start boxplot_valor_causa.png
start kaplan_meier_survival.png
start quebra_estrutural_detectada.png

# No Mac
open distribuicao_tempo_tramitacao.png
open resultado_por_juiz.png

# No Linux
xdg-open distribuicao_tempo_tramitacao.png
```

### 2. Visualize o Relatório HTML

```bash
# Abra o relatório completo no navegador
# Windows
start report_complete.html

# Mac
open report_complete.html

# Linux
xdg-open report_complete.html
```

### 3. Analise os Dados em CSV

```bash
# Veja os resultados da regressão logística
cat resultados_regressao_logistica.csv

# Veja os hazard ratios do modelo Cox
cat hazard_ratios_cox.csv

# Veja o relatório de classificação
cat classification_report.txt
```

## 🔄 Regenerando o Relatório HTML

O script `generate_report_complete.py` está disponível e pode ser executado:

```bash
python generate_report_complete.py
```

Este script:
1. Lê os arquivos CSV existentes
2. Incorpora as imagens PNG
3. Gera um relatório HTML formatado

## 📖 Entendendo os Arquivos

### Arquivos de Visualização (PNG)

1. **`distribuicao_tempo_tramitacao.png`**
   - Mostra quanto tempo os processos levam para serem concluídos
   - Histograma com distribuição de frequência

2. **`resultado_por_juiz.png`**
   - Compara quantos processos cada juiz julga como procedentes/improcedentes
   - Gráfico de barras agrupadas

3. **`boxplot_valor_causa.png`**
   - Compara os valores das causas entre processos procedentes e improcedentes
   - Boxplot mostrando mediana, quartis e outliers

4. **`kaplan_meier_survival.png`**
   - Curva de sobrevivência: probabilidade de um processo ainda estar ativo ao longo do tempo
   - Útil para prever quanto tempo processos similares levam

5. **`quebra_estrutural_detectada.png`**
   - Identifica pontos no tempo onde houve mudança significativa nos padrões
   - Pode indicar mudanças de legislação ou práticas

### Arquivos de Dados (CSV)

1. **`resultados_regressao_logistica.csv`**
   - **Odds Ratio**: Razão de chances
   - Valores > 1: aumentam a chance de procedência
   - Valores < 1: diminuem a chance de procedência

2. **`hazard_ratios_cox.csv`**
   - **Hazard Ratio**: Risco de encerramento do processo
   - Valores > 1: aceleram o encerramento
   - Valores < 1: retardam o encerramento

3. **`classification_report.txt`**
   - **Precision**: De todos que o modelo previu como procedentes, quantos realmente eram?
   - **Recall**: De todos os realmente procedentes, quantos o modelo acertou?
   - **F1-Score**: Média harmônica entre precision e recall

4. **`confusion_matrix.csv`**
   - Matriz 2x2 mostrando:
     - True Positives (TP): Previu procedente, era procedente
     - True Negatives (TN): Previu improcedente, era improcedente
     - False Positives (FP): Previu procedente, era improcedente
     - False Negatives (FN): Previu improcedente, era procedente

5. **`cv_scores.csv`**
   - Scores de validação cruzada (5 folds)
   - Mostra a consistência do modelo em diferentes subconjuntos dos dados

## 🎯 Próximos Passos

Agora que você entende os arquivos, pode:

1. **Analisar os resultados**: Explore os gráficos e tabelas
2. **Ler o tutorial**: Veja `TUTORIAL.md` para aprender a recriar as análises
3. **Modificar o relatório**: Edite `generate_report_complete.py` para personalizar
4. **Criar novas análises**: Use os conceitos para analisar seus próprios dados

## 🆘 Problemas Comuns

### Erro ao executar `generate_report_complete.py`

```
ModuleNotFoundError: No module named 'pandas'
```

**Solução**: Instale as dependências
```bash
pip install pandas
```

### Imagens não aparecem no relatório HTML

**Causa**: O HTML referencia as imagens por caminho relativo

**Solução**: Mantenha o `report_complete.html` no mesmo diretório que as imagens PNG

### Arquivo CSV não encontrado

**Causa**: O script espera que os CSVs existam no mesmo diretório

**Solução**: Certifique-se de que todos os arquivos CSV estão presentes, ou modifique o script para lidar com arquivos ausentes (já está implementado)

## 📚 Recursos Adicionais

- **PROJECT_OVERVIEW.md**: Visão completa do projeto
- **TUTORIAL.md**: Tutorial passo a passo para análise de dados jurimétricos
- **README.md**: Documentação original do projeto

## 💡 Dicas

1. **Explore interativamente**: Use Jupyter Notebook ou Python REPL para explorar os CSVs
2. **Personalize visualizações**: Modifique cores, títulos e estilos nos gráficos
3. **Compare resultados**: Execute múltiplas análises e compare os resultados
4. **Documente mudanças**: Use Git para versionar suas modificações

---

**Pronto!** Você está configurado para começar a trabalhar com o projeto! 🎉
