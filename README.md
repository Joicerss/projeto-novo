# Jurimetria Case — Resultados

Esta pasta contém os resultados gerados pelo script `jurimetria_completa.py`.

## GitHub Copilot Extension Check (Passo 1)

Scripts para verificar se as extensões do GitHub Copilot estão instaladas:

- `check_copilot_extensions.py` — Script Python para verificar extensões
- `check_copilot_extensions.sh` — Script Bash para Unix/Linux/Mac
- `check_copilot_extensions.ps1` — Script PowerShell para Windows
- `COPILOT_CHECK_INSTRUCTIONS.md` — Instruções detalhadas

**Uso rápido:**

```bash
# Python
python3 check_copilot_extensions.py

# Bash (Unix/Linux/Mac)
bash check_copilot_extensions.sh

# PowerShell (Windows)
powershell -ExecutionPolicy Bypass -File check_copilot_extensions.ps1
```

Os scripts verificam se `GitHub.copilot` e `GitHub.copilot-chat` estão instalados e reportam "Encontrei: [status]".

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

1. Garanta que o Python 3.8+ e as dependências estejam instaladas (ver `requirements.txt`).
2. Rode o script principal (no diretório onde o script está):

```powershell
& "C:\Path\to\python.exe" "C:\Users\Usuario\OneDrive\Área de Trabalho\jurimetria_completa.py"
```

3. Os arquivos serão gravados nesta pasta `jurimetria_case/`.

Git local

- Nesta pasta já existe um repositório Git local inicializado e com um commit.
- Para enviar para um remoto: `git remote add origin <URL>` seguido de `git push -u origin main` (forneça credenciais se solicitado).

Observações

- Os dados são simulados para demonstração.
- Se quiser que eu inclua o script de processamento (`processar_dados_csv.py`) ou configure um CI para regenerar relatórios automaticamente, diga e eu faço.
