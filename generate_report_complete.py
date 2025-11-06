import pandas as pd
from pathlib import Path

out = Path(__file__).parent
report_path = out / 'report_complete.html'
# Read CSVs if present
odds_csv = out / 'resultados_regressao_logistica.csv'
cox_csv = out / 'hazard_ratios_cox.csv'

odds_html = '<p><em>Arquivo não encontrado</em></p>'
cox_html = '<p><em>Arquivo não encontrado</em></p>'

if odds_csv.exists():
    df_odds = pd.read_csv(odds_csv)
    odds_html = df_odds.to_html(index=False, classes='table', border=0)

if cox_csv.exists():
    df_cox = pd.read_csv(cox_csv)
    cox_html = df_cox.to_html(index=False, classes='table', border=0)

html = f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Relatório Jurimetria — Completo</title>
  <style>
    body{{font-family:Segoe UI, Roboto, Arial, sans-serif; max-width:1100px;margin:24px auto;color:#111}}
    h1,h2{{color:#0b5;}}
    .row{{display:flex;gap:16px;flex-wrap:wrap}}
    .card{{border:1px solid #ddd;padding:12px;border-radius:6px;flex:1 1 300px}}
    img{{max-width:100%;height:auto;border:1px solid #eee}}
    pre{{background:#f8f8f8;padding:12px;border-radius:6px;overflow:auto}}
    table.table{{border-collapse:collapse;width:100%}}
    table.table th, table.table td{{border:1px solid #ddd;padding:6px;text-align:left}}
  </style>
</head>
<body>
  <h1>Relatório — Jurimetria (Completo)</h1>
  <p>Gerado automaticamente. As figuras abaixo e as tabelas extraídas dos CSVs.</p>

  <h2>Figuras</h2>
  <div class="row">
    <div class="card">
      <h3>Distribuição do tempo de tramitação</h3>
      <img src="distribuicao_tempo_tramitacao.png" alt="Distribuição tempo tramitação"/>
    </div>

    <div class="card">
      <h3>Resultado por juiz</h3>
      <img src="resultado_por_juiz.png" alt="Resultado por juiz"/>
    </div>

    <div class="card">
      <h3>Boxplot do valor da causa</h3>
      <img src="boxplot_valor_causa.png" alt="Boxplot valor da causa"/>
    </div>

    <div class="card">
      <h3>Kaplan–Meier (sobrevivência)</h3>
      <img src="kaplan_meier_survival.png" alt="Kaplan Meier"/>
    </div>

    <div class="card">
      <h3>Detecção de quebra estrutural</h3>
      <img src="quebra_estrutural_detectada.png" alt="Quebra estrutural"/>
    </div>
  </div>

  <h2>Tabelas (CSV)</h2>
  <h3>Regressão Logística — Odds Ratios</h3>
  {odds_html}

  <h3>CoxPH — Sumário (hazard ratios)</h3>
  {cox_html}

  <footer style="margin-top:24px;color:#666;font-size:0.9em">Relatório criado automaticamente pelo gerador — mantenha os arquivos nesta pasta para referência.</footer>
</body>
</html>
'''

report_path.write_text(html, encoding='utf-8')
print('Relatório completo gerado em:', report_path)
