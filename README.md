# Jurimetria Case — Resultados

Esta pasta contém os resultados gerados pelo script `jurimetria_completa.py`.

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

## Guia de Desenvolvimento

### GitHub Copilot

Se você está tendo problemas para instalar ou autenticar o GitHub Copilot (especialmente erros de DNS com `next-waitlist.azurewebsites.net`), consulte nosso guia completo de solução de problemas:

📖 **[Guia de Solução de Problemas — GitHub Copilot](COPILOT_TROUBLESHOOTING.md)**

O guia inclui:
- Instalação da extensão VS Code (método recomendado)
- Autenticação via hotspot/VPN
- Instruções para geração de logs de diagnóstico
- Comparação entre diferentes opções
- FAQ e suporte adicional
