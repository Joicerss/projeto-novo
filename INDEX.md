# ÍNDICE DE DOCUMENTAÇÃO - Projeto Jurimetria

## 🎯 Por onde começar?

Este projeto tem documentação completa em português. Escolha o documento adequado para suas necessidades:

---

## 📖 Documentos Disponíveis

### 1. **README.md** ⭐ COMECE AQUI
- **Público**: Todos
- **Conteúdo**: Visão geral rápida do projeto, início rápido
- **Tempo de leitura**: 5 minutos
- **Link**: [README.md](README.md)

### 2. **PROJECT_OVERVIEW.md** 📋 ENTENDA O PROJETO
- **Público**: Quem quer entender o contexto completo
- **Conteúdo**: 
  - O que é Jurimetria?
  - Estrutura detalhada do projeto
  - Todas as análises realizadas
  - Interpretação dos resultados
  - Tecnologias utilizadas
- **Tempo de leitura**: 15 minutos
- **Link**: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)

### 3. **GETTING_STARTED.md** 🚀 CONFIGURE E EXPLORE
- **Público**: Quem quer configurar o ambiente e explorar os resultados
- **Conteúdo**:
  - Instalação de dependências
  - Como abrir e visualizar os resultados
  - Executar o gerador de relatórios
  - Explicação de cada arquivo
  - Solução de problemas comuns
- **Tempo de leitura**: 10 minutos
- **Link**: [GETTING_STARTED.md](GETTING_STARTED.md)

### 4. **TUTORIAL.md** 🎓 APRENDA PASSO A PASSO
- **Público**: Quem quer aprender a fazer análise jurismétrica do zero
- **Conteúdo**:
  - 7 capítulos completos com código
  - Preparação de dados
  - Análise exploratória
  - Regressão Logística
  - Análise de Sobrevivência (Kaplan-Meier)
  - Modelo Cox
  - Validação de modelos
  - Geração de relatórios
- **Tempo de leitura**: 45+ minutos
- **Link**: [TUTORIAL.md](TUTORIAL.md)

---

## 🗺️ Fluxo de Aprendizado Recomendado

```
1. README.md (5 min)
   ↓
2. PROJECT_OVERVIEW.md (15 min)
   ↓
3. GETTING_STARTED.md (10 min)
   ↓ Configure ambiente e explore
   ↓
4. TUTORIAL.md (45+ min)
   ↓ Aprenda fazendo
   ↓
5. Experimente com seus dados! 🚀
```

---

## 📊 Arquivos do Projeto

### Documentação
- `README.md` - Visão geral
- `PROJECT_OVERVIEW.md` - Detalhes completos
- `GETTING_STARTED.md` - Guia de configuração
- `TUTORIAL.md` - Tutorial completo
- `INDEX.md` - Este arquivo (índice)

### Código
- `generate_report_complete.py` - Gerador de relatórios HTML
- `requirements.txt` - Dependências Python
- `projeto/` - Código R (versões)

### Resultados
- `*.png` - Visualizações (5 gráficos)
- `*.csv` - Dados tabulares (5 tabelas)
- `*.txt` - Relatórios de texto
- `*.html` - Relatórios HTML

---

## 💡 Casos de Uso

### "Quero entender o que é este projeto"
→ Leia: **README.md** → **PROJECT_OVERVIEW.md**

### "Quero ver os resultados rapidamente"
→ Execute:
```bash
# Abra no navegador
open report_complete.html  # Mac
start report_complete.html  # Windows
xdg-open report_complete.html  # Linux
```

### "Quero configurar o ambiente"
→ Leia: **GETTING_STARTED.md**
```bash
pip install -r requirements.txt
python generate_report_complete.py
```

### "Quero aprender a fazer análises similares"
→ Leia: **TUTORIAL.md** (linha por linha, com exemplos de código)

### "Quero contribuir com o projeto"
→ Leia: **PROJECT_OVERVIEW.md** (seção "Próximos Passos")

---

## 🔍 Busca Rápida

### Conceitos
- **O que é Jurimetria?** → PROJECT_OVERVIEW.md
- **Odds Ratio** → TUTORIAL.md, Capítulo 3
- **Hazard Ratio** → TUTORIAL.md, Capítulo 5
- **Kaplan-Meier** → TUTORIAL.md, Capítulo 4
- **Regressão Logística** → TUTORIAL.md, Capítulo 3
- **Modelo Cox** → TUTORIAL.md, Capítulo 5

### Tarefas
- **Instalar dependências** → GETTING_STARTED.md
- **Gerar relatório** → GETTING_STARTED.md ou TUTORIAL.md, Capítulo 7
- **Criar visualizações** → TUTORIAL.md, Capítulo 2
- **Treinar modelo** → TUTORIAL.md, Capítulos 3-5
- **Validar modelo** → TUTORIAL.md, Capítulo 6

### Arquivos
- **Explicação dos PNGs** → GETTING_STARTED.md ou PROJECT_OVERVIEW.md
- **Explicação dos CSVs** → GETTING_STARTED.md ou PROJECT_OVERVIEW.md
- **Como funciona o generate_report_complete.py** → TUTORIAL.md, Capítulo 7

---

## 🆘 Problemas?

### Erro ao importar pandas
```bash
pip install -r requirements.txt
```

### Não consigo abrir o HTML
O arquivo HTML deve estar no mesmo diretório que as imagens PNG.

### Quero mais ajuda
1. Leia a seção "Problemas Comuns" em GETTING_STARTED.md
2. Consulte o tutorial completo em TUTORIAL.md
3. Abra uma issue no GitHub

---

## 🎯 Objetivos de Aprendizado

Após ler toda a documentação, você será capaz de:

- ✅ Entender o que é Jurimetria e suas aplicações
- ✅ Interpretar análises estatísticas de processos judiciais
- ✅ Criar visualizações de dados jurimétricos
- ✅ Treinar modelos preditivos (Regressão Logística)
- ✅ Realizar análise de sobrevivência (Kaplan-Meier)
- ✅ Aplicar modelo de risco proporcional (Cox)
- ✅ Validar modelos com métricas apropriadas
- ✅ Gerar relatórios HTML automatizados
- ✅ Interpretar Odds Ratios e Hazard Ratios
- ✅ Aplicar estes conceitos aos seus próprios dados

---

## 📚 Recursos Externos

- **Python**: https://www.python.org/
- **Pandas**: https://pandas.pydata.org/
- **Scikit-learn**: https://scikit-learn.org/
- **Lifelines**: https://lifelines.readthedocs.io/
- **Matplotlib**: https://matplotlib.org/

---

## ✨ Contribua!

Encontrou um erro na documentação? Tem sugestões de melhoria?
- Abra uma issue
- Envie um pull request
- Entre em contato

---

**Boa leitura e bom aprendizado!** 📖✨
