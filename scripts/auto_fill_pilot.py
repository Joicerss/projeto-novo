"""
Preenche automaticamente (rascunho) as 14 perguntas para os processos do piloto.

Heurísticas aplicadas:
- `pergunta_1`: 'sim' se `itau_flag` for True, caso contrário 'nao'
- `pergunta_2`: 'sim' se `veiculos_flag` for True, caso contrário 'nao'
- `evidencias`: primeiro trecho de `sample_text` (até 500 chars)

Gera: `outputs/pilot_30_filled.xlsx` e `outputs/pilot_30_filled.csv`

Uso: python scripts/auto_fill_pilot.py
"""
import os
from pathlib import Path
import pandas as pd


def load_files(pilot_csv='outputs/pilot_30.csv', model_xlsx='outputs/modelo_respostas.xlsx'):
    p_pilot = Path(pilot_csv)
    p_model = Path(model_xlsx)
    if not p_pilot.exists():
        raise FileNotFoundError(f"Pilot file not found: {pilot_csv}")
    pilot = pd.read_csv(p_pilot, dtype=str)
    if p_model.exists():
        model = pd.read_excel(p_model, dtype=str)
    else:
        # create a default model with pergunta_1..pergunta_14 + evidencias
        cols = [f'pergunta_{i}' for i in range(1,15)] + ['evidencias']
        model = pd.DataFrame(columns=cols)
    return pilot, model


def fill_row(row):
    # basic heuristics
    filled = {}
    itau = str(row.get('itau_flag','')).lower() in ('true','1','sim','yes','y','t')
    veic = str(row.get('veiculos_flag','')).lower() in ('true','1','sim','yes','y','t')
    filled['pergunta_1'] = 'sim' if itau else 'nao'
    filled['pergunta_2'] = 'sim' if veic else 'nao'
    # leave other perguntas blank for manual review
    for i in range(3,15):
        filled[f'pergunta_{i}'] = ''
    txt = str(row.get('sample_text','') or '')
    evid = (txt[:500] + '...') if len(txt) > 500 else txt
    filled['evidencias'] = evid
    # always include numero_processo column if present
    if 'numero_processo' in row.index:
        filled['numero_processo'] = row.get('numero_processo')
    elif 'numero_proc_norm' in row.index:
        filled['numero_processo'] = row.get('numero_proc_norm')
    else:
        filled['numero_processo'] = ''
    return filled


def main():
    pilot, model = load_files()
    rows = []
    for _, r in pilot.iterrows():
        filled = fill_row(r)
        rows.append(filled)
    df_out = pd.DataFrame(rows)
    out_dir = Path('outputs')
    out_dir.mkdir(exist_ok=True)
    out_xlsx = out_dir / 'pilot_30_filled.xlsx'
    out_csv = out_dir / 'pilot_30_filled.csv'
    df_out.to_excel(out_xlsx, index=False)
    df_out.to_csv(out_csv, index=False)
    print(f'Preenchimento automático salvo: {out_xlsx} (linhas={len(df_out)})')


if __name__ == '__main__':
    main()
