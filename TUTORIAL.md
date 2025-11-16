# Tutorial Passo a Passo - Análise Jurismétrica

Este tutorial vai te ensinar a fazer análise jurismétrica do zero, usando os conceitos do projeto.

## 📚 Índice

1. [Preparação dos Dados](#1-preparação-dos-dados)
2. [Análise Exploratória](#2-análise-exploratória)
3. [Regressão Logística](#3-regressão-logística)
4. [Análise de Sobrevivência](#4-análise-de-sobrevivência)
5. [Modelo Cox](#5-modelo-cox)
6. [Validação do Modelo](#6-validação-do-modelo)
7. [Geração de Relatórios](#7-geração-de-relatórios)

---

## 1. Preparação dos Dados

### 1.1 Estrutura de Dados Esperada

Um dataset jurismétrico típico contém:

```python
import pandas as pd
import numpy as np

# Exemplo de estrutura de dados
dados = {
    'processo_id': [1, 2, 3, 4, 5],
    'juiz': ['Juiz A', 'Juiz B', 'Juiz A', 'Juiz C', 'Juiz B'],
    'classe': ['Trabalhista', 'Criminal', 'Cível', 'Trabalhista', 'Criminal'],
    'valor_causa': [10000, 5000, 50000, 15000, 8000],
    'tempo_tramitacao_dias': [180, 90, 365, 200, 120],
    'resultado': [1, 0, 1, 1, 0]  # 1 = Procedente, 0 = Improcedente
}

df = pd.DataFrame(dados)
print(df.head())
```

### 1.2 Limpeza e Preparação

```python
# Converter tipos de dados
df['valor_causa'] = df['valor_causa'].astype(float)
df['tempo_tramitacao_dias'] = df['tempo_tramitacao_dias'].astype(int)

# Criar variáveis categóricas
df['faixa_valor'] = pd.cut(df['valor_causa'], 
                            bins=[0, 10000, 30000, np.inf],
                            labels=['Baixo', 'Médio', 'Alto'])

# Verificar dados faltantes
print(df.isnull().sum())

# Remover ou imputar dados faltantes
df = df.dropna()  # ou df.fillna(valor)
```

---

## 2. Análise Exploratória

### 2.1 Distribuição do Tempo de Tramitação

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
plt.hist(df['tempo_tramitacao_dias'], bins=30, edgecolor='black', alpha=0.7)
plt.xlabel('Tempo de Tramitação (dias)')
plt.ylabel('Frequência')
plt.title('Distribuição do Tempo de Tramitação')
plt.grid(axis='y', alpha=0.3)
plt.savefig('distribuicao_tempo_tramitacao.png', dpi=100, bbox_inches='tight')
plt.show()
```

**O que observar:**
- A maioria dos processos leva quanto tempo?
- Existem outliers (processos muito rápidos ou muito lentos)?
- A distribuição é normal ou assimétrica?

### 2.2 Resultado por Juiz

```python
plt.figure(figsize=(10, 6))
resultado_juiz = df.groupby(['juiz', 'resultado']).size().unstack(fill_value=0)
resultado_juiz.plot(kind='bar', stacked=False)
plt.xlabel('Juiz')
plt.ylabel('Quantidade de Processos')
plt.title('Resultado por Juiz')
plt.legend(['Improcedente', 'Procedente'])
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('resultado_por_juiz.png', dpi=100, bbox_inches='tight')
plt.show()
```

**O que observar:**
- Algum juiz julga mais procedentes que outros?
- A distribuição é uniforme ou há padrões?

### 2.3 Boxplot do Valor da Causa

```python
plt.figure(figsize=(10, 6))
df['resultado_label'] = df['resultado'].map({0: 'Improcedente', 1: 'Procedente'})
sns.boxplot(data=df, x='resultado_label', y='valor_causa')
plt.xlabel('Resultado')
plt.ylabel('Valor da Causa (R$)')
plt.title('Distribuição do Valor da Causa por Resultado')
plt.savefig('boxplot_valor_causa.png', dpi=100, bbox_inches='tight')
plt.show()
```

**O que observar:**
- Processos com valores maiores têm mais chance de serem procedentes?
- Existem outliers significativos?

---

## 3. Regressão Logística

### 3.1 Por que usar Regressão Logística?

A regressão logística prevê a probabilidade de um evento binário (procedente/improcedente).

### 3.2 Preparação dos Dados

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Codificar variáveis categóricas
df_encoded = df.copy()
le_juiz = LabelEncoder()
le_classe = LabelEncoder()
le_faixa = LabelEncoder()

df_encoded['juiz_encoded'] = le_juiz.fit_transform(df['juiz'])
df_encoded['classe_encoded'] = le_classe.fit_transform(df['classe'])
df_encoded['faixa_valor_encoded'] = le_faixa.fit_transform(df['faixa_valor'])

# Selecionar features e target
X = df_encoded[['juiz_encoded', 'classe_encoded', 'faixa_valor_encoded', 'tempo_tramitacao_dias']]
y = df_encoded['resultado']

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

### 3.3 Treinar o Modelo

```python
# Treinar modelo
modelo = LogisticRegression(random_state=42, max_iter=1000)
modelo.fit(X_train, y_train)

# Calcular odds ratios
odds_ratios = np.exp(modelo.coef_[0])

# Criar DataFrame com resultados
resultados = pd.DataFrame({
    'Variável': X.columns,
    'Odds Ratio': odds_ratios
})

print(resultados)
resultados.to_csv('resultados_regressao_logistica.csv', index=False)
```

### 3.4 Interpretação dos Odds Ratios

- **OR > 1**: Aumenta a chance de procedência
  - Ex: OR = 1.5 → 50% mais chance
- **OR < 1**: Diminui a chance de procedência
  - Ex: OR = 0.8 → 20% menos chance
- **OR = 1**: Não tem efeito

---

## 4. Análise de Sobrevivência (Kaplan-Meier)

### 4.1 Conceito

A análise de sobrevivência estuda o tempo até um evento (no nosso caso, o encerramento do processo).

### 4.2 Preparar Dados para Análise de Sobrevivência

```python
from lifelines import KaplanMeierFitter

# Criar dados de sobrevivência
# event: 1 = processo encerrado, 0 = ainda em andamento (censurado)
df['event'] = 1  # Assumindo que todos foram encerrados

# Inicializar o modelo
kmf = KaplanMeierFitter()
kmf.fit(df['tempo_tramitacao_dias'], df['event'])
```

### 4.3 Plotar a Curva de Kaplan-Meier

```python
plt.figure(figsize=(10, 6))
kmf.plot_survival_function()
plt.xlabel('Tempo (dias)')
plt.ylabel('Probabilidade de Sobrevivência')
plt.title('Curva de Kaplan-Meier: Probabilidade do Processo Ainda Estar Ativo')
plt.grid(True, alpha=0.3)
plt.savefig('kaplan_meier_survival.png', dpi=100, bbox_inches='tight')
plt.show()
```

**Interpretação:**
- **Y = 1 (100%)**: No início, todos os processos estão ativos
- **Y = 0.5 (50%)**: Metade dos processos ainda está ativa
- **Y = 0 (0%)**: Todos os processos foram encerrados

### 4.4 Comparar por Categoria

```python
plt.figure(figsize=(10, 6))

for classe in df['classe'].unique():
    mask = df['classe'] == classe
    kmf.fit(df[mask]['tempo_tramitacao_dias'], df[mask]['event'], label=classe)
    kmf.plot_survival_function()

plt.xlabel('Tempo (dias)')
plt.ylabel('Probabilidade de Sobrevivência')
plt.title('Curvas de Kaplan-Meier por Classe de Processo')
plt.legend()
plt.savefig('kaplan_meier_por_classe.png', dpi=100, bbox_inches='tight')
plt.show()
```

---

## 5. Modelo Cox (Risco Proporcional)

### 5.1 Por que usar o Modelo Cox?

O modelo Cox identifica quais fatores aceleram ou retardam o encerramento dos processos.

### 5.2 Treinar o Modelo Cox

```python
from lifelines import CoxPHFitter

# Preparar dados
df_cox = df_encoded[['juiz_encoded', 'classe_encoded', 'faixa_valor_encoded', 
                      'tempo_tramitacao_dias', 'event']].copy()

# Treinar modelo
cph = CoxPHFitter()
cph.fit(df_cox, duration_col='tempo_tramitacao_dias', event_col='event')

# Ver sumário
print(cph.summary)

# Salvar hazard ratios
hazard_ratios = pd.DataFrame({
    'Variável': cph.summary.index,
    'Hazard Ratio': np.exp(cph.summary['coef'])
})
hazard_ratios.to_csv('hazard_ratios_cox.csv', index=False)
```

### 5.3 Interpretação dos Hazard Ratios

- **HR > 1**: Acelera o encerramento (processo termina mais rápido)
- **HR < 1**: Retarda o encerramento (processo demora mais)
- **HR = 1**: Não tem efeito no tempo

**Exemplo:**
- HR = 1.5 → 50% mais risco de encerrar (termina mais rápido)
- HR = 0.7 → 30% menos risco de encerrar (demora mais)

---

## 6. Validação do Modelo

### 6.1 Previsões e Métricas

```python
from sklearn.metrics import classification_report, confusion_matrix

# Fazer previsões
y_pred = modelo.predict(X_test)

# Relatório de classificação
report = classification_report(y_test, y_pred)
print(report)

# Salvar relatório
with open('classification_report.txt', 'w') as f:
    f.write('Classification report (test)\n')
    f.write(report)

# Matriz de confusão
cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(cm)
cm_df.to_csv('confusion_matrix.csv', index=False)
print("\nMatriz de Confusão:")
print(cm)
```

### 6.2 Validação Cruzada

```python
from sklearn.model_selection import cross_val_score

# Validação cruzada com 5 folds
cv_scores = cross_val_score(modelo, X, y, cv=5, scoring='accuracy')

print(f"Scores CV: {cv_scores}")
print(f"Média: {cv_scores.mean():.2f}")
print(f"Desvio Padrão: {cv_scores.std():.2f}")

# Salvar scores
cv_df = pd.DataFrame({'fold': range(1, 6), 'accuracy': cv_scores})
cv_df.to_csv('cv_scores.csv', index=False)
```

### 6.3 Interpretando as Métricas

**Precision (Precisão):**
- De todos que previmos como procedentes, quantos realmente eram?
- Alta precisão = poucas falsas alarmes

**Recall (Revocação/Sensibilidade):**
- De todos os realmente procedentes, quantos conseguimos identificar?
- Alto recall = poucas oportunidades perdidas

**F1-Score:**
- Média harmônica entre precision e recall
- Balanceia os dois aspectos

**Accuracy (Acurácia):**
- % de previsões corretas no total
- Pode ser enganosa com classes desbalanceadas

---

## 7. Geração de Relatórios

### 7.1 Relatório HTML Simples

```python
# Já existe no projeto: generate_report_complete.py
# Execute:
python generate_report_complete.py
```

### 7.2 Relatório HTML Personalizado

```python
from pathlib import Path

def gerar_relatorio_customizado():
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Meu Relatório Jurismétrico</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2c3e50; }}
            .metric {{ 
                background: #ecf0f1; 
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 5px; 
            }}
            img {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>
        <h1>Análise Jurismétrica - Relatório Customizado</h1>
        
        <h2>Métricas Principais</h2>
        <div class="metric">
            <strong>Acurácia do Modelo:</strong> {accuracy:.2%}
        </div>
        
        <h2>Visualizações</h2>
        <img src="distribuicao_tempo_tramitacao.png" alt="Distribuição">
        <img src="resultado_por_juiz.png" alt="Resultado por Juiz">
        
        <h2>Conclusões</h2>
        <p>Adicione suas conclusões aqui...</p>
    </body>
    </html>
    """
    
    Path('relatorio_customizado.html').write_text(html, encoding='utf-8')
    print("Relatório gerado!")

# Se você tiver a acurácia calculada:
# accuracy = modelo.score(X_test, y_test)
# gerar_relatorio_customizado()
```

---

## 🎯 Exercícios Práticos

### Exercício 1: Análise Básica
1. Carregue os CSVs existentes do projeto
2. Calcule estatísticas descritivas (média, mediana, desvio padrão)
3. Crie um gráfico de sua escolha

### Exercício 2: Previsão
1. Simule um novo processo com características específicas
2. Use o modelo treinado para prever o resultado
3. Calcule a probabilidade de procedência

### Exercício 3: Comparação
1. Compare diferentes juízes ou classes
2. Identifique qual tem maior taxa de procedência
3. Crie uma visualização para apresentar os resultados

### Exercício 4: Relatório
1. Modifique o `generate_report_complete.py`
2. Adicione uma nova seção ou gráfico
3. Personalize as cores e estilos

---

## 🚀 Próximos Passos

Agora que você completou o tutorial:

1. **Experimente com dados reais** (respeitando privacidade/LGPD)
2. **Adicione novas variáveis** (comarca, ano, advogado, etc.)
3. **Teste outros modelos** (Random Forest, XGBoost, etc.)
4. **Implemente feature engineering** (criar novas variáveis derivadas)
5. **Automatize o pipeline** (scripts para ETL, treinamento, deploy)

---

## 📚 Recursos Adicionais

- **Scikit-learn Documentation**: https://scikit-learn.org/
- **Lifelines Documentation**: https://lifelines.readthedocs.io/
- **Pandas Documentation**: https://pandas.pydata.org/
- **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/

---

**Parabéns!** Você agora sabe como fazer análise jurismétrica completa! 🎉
