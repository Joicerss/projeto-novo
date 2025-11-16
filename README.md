# Projeto Jurimetria — Análise de Dados Judiciais

Este projeto demonstra análises jurimétricas completas usando técnicas de ciência de dados aplicadas ao sistema judicial.

---

## 🚀 **[COMECE AQUI!](COMECE_AQUI.md)** ⭐

**Novo no projeto?** Leia o guia [COMECE_AQUI.md](COMECE_AQUI.md) para começar passo a passo!

---

## 📚 Documentação Completa

**[📖 ÍNDICE DA DOCUMENTAÇÃO](INDEX.md)** - Guia completo de toda a documentação disponível

### Documentos Principais

- **[COMECE AQUI](COMECE_AQUI.md)** ⭐ - Ponto de partida para iniciantes
- **[Visão Geral do Projeto](PROJECT_OVERVIEW.md)** - Entenda o que é o projeto, estrutura e conceitos
- **[Guia de Início Rápido](GETTING_STARTED.md)** - Configure o ambiente e comece a trabalhar
- **[Tutorial Passo a Passo](TUTORIAL.md)** - Aprenda a fazer análise jurismétrica do zero

## 🎯 O que é Jurimetria?

Jurimetria é a aplicação de métodos estatísticos e análise de dados ao Direito. Este projeto demonstra:
- Análise descritiva de processos judiciais
- Modelagem preditiva (Regressão Logística)
- Análise de sobrevivência (Kaplan-Meier)
- Modelo de risco proporcional (Cox)
- Validação de modelos e métricas de performance

## 🚀 Início Rápido

```bash
# Clone o repositório
git clone https://github.com/Joicerss/projeto-novo.git
cd projeto-novo

# Instale as dependências
pip install -r requirements.txt

# Gere o relatório HTML
python generate_report_complete.py

# Abra o relatório no navegador
# Windows: start report_complete.html
# Mac: open report_complete.html
# Linux: xdg-open report_complete.html
```

## 📊 Resultados

Esta pasta contém os resultados gerados pelo script `jurimetria_completa.py`.

### Visualizações (PNG)

- `distribuicao_tempo_tramitacao.png` — histograma do tempo de tramitação
- `resultado_por_juiz.png` — contagem de resultados por juiz
- `boxplot_valor_causa.png` — boxplot do valor da causa por resultado
- `kaplan_meier_survival.png` — curva de sobrevivência Kaplan–Meier
- `quebra_estrutural_detectada.png` — gráfico com a quebra estrutural detectada (simulada)

### Dados (CSV)

- `resultados_regressao_logistica.csv` — odds ratios / coeficientes da regressão logística
- `hazard_ratios_cox.csv` — sumário do modelo CoxPH (hazard ratios)
- `classification_report.txt` — relatório de classificação (texto) do conjunto de teste
- `confusion_matrix.csv` — matriz de confusão em formato CSV
- `cv_scores.csv` — valores de acurácia por fold do cross-validation

### Relatórios (HTML)

- `report_complete.html` — relatório HTML completo (figuras + tabelas)
- `report.html` — relatório HTML simples

## 🛠️ Tecnologias

- **Python 3.8+** com pandas, scikit-learn, lifelines, matplotlib
- **R** (projeto configurado)
- **GitHub Actions** (CI/CD configurado para publicação de pacotes)

## 📖 Como Usar

### Visualizar Resultados Existentes

```bash
# Abrir relatório completo
open report_complete.html  # Mac
start report_complete.html  # Windows
xdg-open report_complete.html  # Linux
```

### Regenerar Relatório

```bash
python generate_report_complete.py
```

### Executar Análises Completas

O script principal `jurimetria_completa.py` não está incluído no repositório. 
Para recriar as análises, veja o [Tutorial](TUTORIAL.md) que ensina passo a passo.

## 🎓 Aprendizado

Este projeto é educacional e usa **dados simulados**. Ideal para:
- Estudantes de Direito interessados em Jurimetria
- Cientistas de Dados explorando aplicações jurídicas
- Profissionais do Direito querendo entender análise de dados
- Pesquisadores em Jurimetria

## 📝 Estrutura do Projeto

```
projeto-novo/
├── README.md                          # Este arquivo
├── PROJECT_OVERVIEW.md                # Visão geral detalhada
├── GETTING_STARTED.md                 # Guia de início
├── TUTORIAL.md                        # Tutorial passo a passo
├── requirements.txt                   # Dependências Python
├── generate_report_complete.py        # Gerador de relatório
├── projeto/                           # Código R (versões)
└── [resultados...]                    # PNG, CSV, HTML
```


## 🔧 Reprodução

Para reproduzir as análises do zero:

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Siga o tutorial:**
   Veja [TUTORIAL.md](TUTORIAL.md) para aprender a criar todas as análises passo a passo

3. **Ou execute o script principal** (se disponível):
   ```bash
   python jurimetria_completa.py
   ```

## 🤝 Contribuindo

Contribuições são bem-vindas! Áreas de interesse:
- Adicionar novas análises estatísticas
- Melhorar visualizações
- Otimizar modelos preditivos
- Adicionar testes automatizados
- Melhorar documentação

## 📜 Licença

Este projeto é educacional e usa dados simulados.

## 🆘 Suporte

Se tiver dúvidas:
1. Leia o [Tutorial](TUTORIAL.md)
2. Consulte a [Visão Geral](PROJECT_OVERVIEW.md)
3. Abra uma issue no GitHub

---

**Nota**: Este projeto usa dados simulados para fins educacionais. 
Para trabalhar com dados reais, certifique-se de seguir as regulamentações de privacidade (LGPD/GDPR).

