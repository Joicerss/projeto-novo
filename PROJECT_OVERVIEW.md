# Visão Geral do Projeto - Jurimetria

## 📋 O que é este projeto?

Este é um **projeto de Jurimetria** - a aplicação de métodos estatísticos e análise de dados ao sistema jurídico. O projeto analisa dados de processos judiciais para identificar padrões, prever resultados e entender o comportamento do sistema judicial.

## 🎯 Objetivo

O objetivo principal é demonstrar técnicas de análise jurisprudencial usando:
- **Análise descritiva**: entender a distribuição dos dados
- **Modelagem preditiva**: prever resultados de processos
- **Análise de sobrevivência**: estudar a duração dos processos
- **Detecção de padrões**: identificar mudanças estruturais ao longo do tempo

## 📁 Estrutura do Projeto

```
projeto-novo/
├── README.md                              # Documentação principal
├── projeto-novo.Rproj                     # Projeto R
├── scriprojetoR.R                         # Script R (vazio)
│
├── projeto/                               # Diretório com versões do projeto
│   ├── versao.R                          # Versão 1 do projeto
│   ├── versao1.R                         # Versão 1 do projeto
│   └── token                             # Arquivo de token
│
├── generate_report_complete.py           # Script Python para gerar relatório HTML
│
└── Arquivos de Resultados (CSV, PNG, HTML):
    ├── distribuicao_tempo_tramitacao.png    # Histograma do tempo de tramitação
    ├── resultado_por_juiz.png                # Contagem de resultados por juiz
    ├── boxplot_valor_causa.png               # Boxplot do valor da causa
    ├── kaplan_meier_survival.png             # Curva de sobrevivência
    ├── quebra_estrutural_detectada.png       # Gráfico de quebra estrutural
    ├── resultados_regressao_logistica.csv    # Odds ratios da regressão
    ├── hazard_ratios_cox.csv                 # Hazard ratios do modelo Cox
    ├── classification_report.txt             # Relatório de classificação
    ├── confusion_matrix.csv                  # Matriz de confusão
    ├── cv_scores.csv                         # Scores de validação cruzada
    ├── report.html                           # Relatório HTML simples
    └── report_complete.html                  # Relatório HTML completo
```

## 🔬 Análises Realizadas

### 1. **Análise Descritiva**
- **Tempo de tramitação**: Distribuição de quanto tempo os processos levam
- **Resultado por juiz**: Como cada juiz decide os casos
- **Valor da causa**: Análise dos valores envolvidos nos processos

### 2. **Modelagem Preditiva**
- **Regressão Logística**: Prevê o resultado do processo (procedente/improcedente)
- **Odds Ratios**: Mostra quais fatores influenciam mais o resultado
  - Juiz responsável
  - Classe do processo (Trabalhista, Criminal, etc.)
  - Faixa de valor da causa
  - Tempo de tramitação

### 3. **Análise de Sobrevivência (Kaplan-Meier)**
- Estuda quanto tempo os processos "sobrevivem" (permanecem ativos)
- Curvas de sobrevivência para diferentes categorias

### 4. **Modelo de Risco Proporcional de Cox (CoxPH)**
- Identifica fatores que aceleram ou retardam o fim dos processos
- **Hazard Ratios**: Risco relativo de encerramento

### 5. **Detecção de Quebra Estrutural**
- Identifica mudanças nos padrões ao longo do tempo
- Útil para detectar mudanças de legislação ou práticas judiciais

### 6. **Validação do Modelo**
- **Classification Report**: Precision, Recall, F1-Score
- **Confusion Matrix**: Acertos e erros do modelo
- **Cross-Validation**: Validação cruzada com 5 folds

## 📊 Principais Resultados

### Regressão Logística - Odds Ratios
```
Variável                    | Odds Ratio | Interpretação
---------------------------|------------|----------------------------------
juiz_Juiz B                | 1.37       | 37% mais chance de procedência
classe_Trabalhista         | 1.15       | 15% mais chance de procedência
faixa_valor_Alto           | 1.07       | 7% mais chance de procedência
tempo_tramitacao_dias      | 1.04       | Quanto maior o tempo, maior chance
juiz_Juiz C                | 1.01       | Praticamente neutro
classe_Criminal            | 1.00       | Categoria de referência
faixa_valor_Médio          | 0.84       | 16% menos chance de procedência
```

### Performance do Modelo
```
Acurácia: 53%
- Classe 0 (Improcedente): Precision 0.45, Recall 0.83
- Classe 1 (Procedente):   Precision 0.75, Recall 0.33
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal para análise
- **Pandas**: Manipulação de dados
- **Scikit-learn**: Modelagem preditiva
- **Lifelines**: Análise de sobrevivência (Kaplan-Meier, Cox)
- **Matplotlib/Seaborn**: Visualização de dados
- **R**: Ambiente alternativo (projeto R configurado)

## 📝 Dados

**Importante**: Os dados são **simulados** para demonstração. Não são dados reais de processos judiciais.

Variáveis típicas incluem:
- Juiz responsável
- Classe do processo (Trabalhista, Criminal, Cível, etc.)
- Valor da causa
- Tempo de tramitação
- Resultado (procedente/improcedente)
- Data de início/fim

## 🎓 Conceitos de Jurimetria

### O que é Jurimetria?
Jurimetria é a aplicação de métodos quantitativos ao Direito, permitindo:
- Prever resultados de processos
- Identificar padrões de decisão
- Otimizar estratégias jurídicas
- Medir a eficiência do sistema judicial
- Fundamentar políticas públicas com dados

### Aplicações Práticas
1. **Advocacia**: Avaliar chances de sucesso de um caso
2. **Gestão Judicial**: Identificar gargalos e otimizar recursos
3. **Políticas Públicas**: Embasar reformas no sistema judicial
4. **Pesquisa Acadêmica**: Estudar o comportamento do sistema jurídico

## 🔄 Status do Projeto

- ✅ Análises estatísticas implementadas
- ✅ Visualizações geradas
- ✅ Modelos preditivos treinados
- ✅ Relatórios HTML automatizados
- ⚠️ Script principal de análise não está presente (mencionado como `jurimetria_completa.py`)
- ⚠️ Arquivo de dados brutos não está presente
- ⚠️ Requirements.txt não está presente

## 📚 Próximos Passos Possíveis

1. **Adicionar o script principal**: Incluir `jurimetria_completa.py` que gera todas as análises
2. **Adicionar requirements.txt**: Documentar dependências Python
3. **Melhorar o modelo**: Acurácia de 53% pode ser melhorada
4. **Adicionar mais análises**: Análise de tendências temporais, clusterização, etc.
5. **Automatizar com CI/CD**: GitHub Actions para regenerar relatórios automaticamente
6. **Adicionar dados de exemplo**: Incluir CSV com dados simulados

## 🤝 Como Contribuir

Este projeto está em desenvolvimento. Contribuições são bem-vindas para:
- Melhorar a documentação
- Adicionar novas análises
- Otimizar os modelos
- Corrigir bugs
- Adicionar testes automatizados

---

**Nota**: Este é um projeto educacional/demonstrativo usando dados simulados.
