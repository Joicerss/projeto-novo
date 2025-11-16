# Projeto de Jurimetria — Análise e Coleta de Dados Judiciais

Este repositório contém ferramentas para análise jurimetrica e coleta automatizada de dados de processos judiciais, com foco em recuperação judicial no setor de veículos pesados.

## 📂 Estrutura do Projeto

### Análise de Dados (Resultados Existentes)

Esta pasta contém os resultados gerados pelo script `jurimetria_completa.py`.

### Análise de Dados (Resultados Existentes)

Arquivos principais:

- `distribuicao_tempo_tramitacao.png` — histograma do tempo de tramitação.
- `resultado_por_juiz.png` — contagem de resultados por juiz.
- `boxplot_valor_causa.png` — boxplot do valor da causa por resultado.
- `kaplan_meier_survival.png` — curva de sobrevivência Kaplan–Meier.
- `quebra_estrutural_detectada.png` — gráfico com a quebra estrutural detectada (simulada).
- `resultados_regressao_logistica.csv` — odds ratios / coeficientes da regressão logística.
- `hazard_ratios_cox.csv` — sumário do modelo CoxPH (hazard ratios).
- `classification_report.txt` — relatório de classificação (texto) do conjunto de teste.
- `confusion_matrix.csv` — matriz de confusão em formato CSV.
- `cv_scores.csv` — valores de acurácia por fold do cross-validation.
- `report_complete.html` — relatório HTML completo (figuras + tabelas).

Como reproduzir a análise:

1. Instale as dependências Python (ver `requirements.txt`)
2. Execute o gerador de relatório:

```bash
python generate_report_complete.py
```

3. Os arquivos serão atualizados no diretório atual.

### Coleta Automatizada de Dados (Novo!)

Sistema automatizado para coleta de dados de processos judiciais dos Tribunais de Justiça brasileiros.

**Localização**: [`coleta_judicial/`](coleta_judicial/)

**Características**:
- Busca automatizada em tribunais (TJSP e outros)
- Foco em processos de recuperação judicial envolvendo Itaú e veículos pesados
- Exportação em múltiplos formatos (CSV, JSON, Excel)
- Arquitetura modular e extensível
- Logging detalhado e tratamento de erros

**Início rápido**:
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar coleta
cd coleta_judicial
python main_collector.py
```

Veja a [documentação completa](coleta_judicial/README.md) para mais informações.

## 🚀 Como Usar

### Análise de Dados Existentes

1. Garanta que o Python 3.8+ e as dependências estejam instaladas (ver `requirements.txt`).
2. Rode o script principal (no diretório onde o script está):

```bash
python generate_report_complete.py
```

### Coleta de Novos Dados

```bash
cd coleta_judicial
python main_collector.py
```

Ou use exemplos interativos:

```bash
cd coleta_judicial
python examples.py
```

## 📦 Dependências

Instale todas as dependências necessárias:

```bash
pip install -r requirements.txt
```

Principais pacotes:
- pandas - Análise de dados
- requests - Requisições HTTP
- beautifulsoup4 - Parsing HTML
- selenium/playwright - Automação web (opcional)
- openpyxl - Exportação Excel

## 🎯 Objetivos do Projeto

### Questões de Pesquisa

1. Quais são os principais motivos que levam empresas do setor de veículos pesados a entrarem em recuperação judicial?
2. Qual é a taxa de sucesso das recuperações judiciais neste setor?
3. Qual o tempo médio de tramitação desses processos?
4. Quais são as garantias mais comumente oferecidas?
5. Qual o papel dos bancos (especialmente Itaú) nesses processos?
6. Quais são os principais credores além dos bancos?
7. Há padrões regionais ou temporais nos pedidos de recuperação?

## 📊 Arquivos de Análise

- `distribuicao_tempo_tramitacao.png` — histograma do tempo de tramitação.
- `resultado_por_juiz.png` — contagem de resultados por juiz.
- `boxplot_valor_causa.png` — boxplot do valor da causa por resultado.
- `kaplan_meier_survival.png` — curva de sobrevivência Kaplan–Meier.
- `quebra_estrutural_detectada.png` — gráfico com a quebra estrutural detectada (simulada).
- `resultados_regressao_logistica.csv` — odds ratios / coeficientes da regressão logística.
- `hazard_ratios_cox.csv` — sumário do modelo CoxPH (hazard ratios).
- `classification_report.txt` — relatório de classificação (texto) do conjunto de teste.
- `confusion_matrix.csv` — matriz de confusão em formato CSV.
- `cv_scores.csv` — valores de acurácia por fold do cross-validation.
- `report_complete.html` — relatório HTML completo (figuras + tabelas).

## 🔧 Configuração

### Coleta de Dados

Edite `coleta_judicial/config.py` para personalizar:
- Bancos a buscar
- Palavras-chave
- Tribunais
- Período de busca
- Formato de saída

## 📝 Git e Controle de Versão

- Este repositório está configurado com Git
- Use `.gitignore` para evitar commitar dados sensíveis ou temporários
- Diretórios de saída são ignorados por padrão

## ⚠️ Observações Importantes

### Sobre os Dados de Análise
- Os dados de análise existentes são simulados para demonstração

### Sobre a Coleta de Dados
- **Respeite robots.txt** e políticas dos tribunais
- **Use com responsabilidade** - não sobrecarregue servidores
- **LGPD** - Ao lidar com dados pessoais, siga a legislação
- **Dados públicos** - Colete apenas informações públicas
- Alguns tribunais requerem CAPTCHA ou autenticação

## 🤝 Contribuindo

Contribuições são bem-vindas! Áreas prioritárias:
1. Implementação completa dos parsers de tribunais
2. Scrapers para tribunais adicionais
3. Testes automatizados
4. Análise estatística dos dados coletados

## 📄 Licença

Projeto desenvolvido para fins acadêmicos e de pesquisa em jurimetria.

---

**Dúvidas?** Consulte a documentação em [`coleta_judicial/README.md`](coleta_judicial/README.md)
