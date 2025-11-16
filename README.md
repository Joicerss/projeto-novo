# Jurimetria Case — Resultados

Esta pasta contém os resultados gerados pelo script `jurimetria_completa.py`.

## 🔐 Autenticação / Authentication

Este projeto agora possui um sistema de autenticação baseado em token para proteger o acesso à geração de relatórios.

**Para mais informações, consulte: [AUTHENTICATION.md](AUTHENTICATION.md)**

### Início Rápido / Quick Start

1. Gerar token / Generate token:
   ```bash
   python token_manager.py gerar
   ```

2. Gerar relatório com autenticação / Generate report with authentication:
   ```bash
   python generate_report_complete.py <seu_token>
   ```

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

Como reproduzir:

1. Garanta que o Python 3.8+ e as dependências estejam instaladas:
   ```bash
   pip install pandas
   ```

2. Configure a autenticação (primeira vez):
   ```bash
   python token_manager.py gerar
   ```

3. Gere o relatório fornecendo o token:
   ```bash
   python generate_report_complete.py <seu_token>
   ```

Git local

- Nesta pasta já existe um repositório Git local inicializado e com um commit.
- Para enviar para um remoto: `git remote add origin <URL>` seguido de `git push -u origin main` (forneça credenciais se solicitado).

Observações

- Os dados são simulados para demonstração.
- Se quiser que eu inclua o script de processamento (`processar_dados_csv.py`) ou configure um CI para regenerar relatórios automaticamente, diga e eu faço.
