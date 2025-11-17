"""
Pipeline: consolida múltiplos CSVs, normaliza número do processo e gera flags iniciais.
Gera: outputs/consolidado_flags.csv e outputs/consolidado_flags.json

Uso: python starter_scripts/01_pipeline_responder_14_questoes.py
"""
import os
import re
import json
from glob import glob
from pathlib import Path
import pandas as pd


ITAU_PATTERNS = [r"\bita[uú]?\b", r"itau unibanco", r"itauunibanco", r"\bitau\b"]
VEIC_PATTERNS = [
    "caminh", "carret", "onibus", "ônibus", "bitrem", "rodotrem", "semirreboque",
    "reboque", "implemento", "basculante", "carreta", "cavalo-mec", "veiculo", "veículos"
]


def normalize_proc(s: str) -> str:
    if pd.isna(s):
        return ""
    s = str(s)
    # remove non-digits
    digits = re.sub(r"\D", "", s)
    return digits


def text_has_any(text: str, patterns) -> bool:
    if not isinstance(text, str):
        return False
    t = text.lower()
    for p in patterns:
        if isinstance(p, str):
            if p in t:
                return True
        else:
            # regex
            if re.search(p, t):
                return True
    return False


def load_csvs(base_dir: str = "."):
    paths = []
    # Only look inside the `data/` directory to avoid picking CSVs from venv or packages
    p = Path(base_dir) / "data"
    if p.exists() and p.is_dir():
        paths.extend([str(x) for x in p.glob("**/*.csv")])
    else:
        print("Atenção: pasta 'data/' não encontrada — nenhum CSV será carregado.")
    # dedupe
    unique = []
    for f in paths:
        if f not in unique:
            unique.append(f)
    dfs = []
    for f in unique:
        try:
            df = pd.read_csv(f, dtype=str, encoding="utf-8")
        except Exception:
            try:
                df = pd.read_csv(f, dtype=str, encoding="latin1")
            except Exception:
                print(f"Falha ao ler {f}, pulando.")
                continue
        df['__source'] = os.path.basename(f)
        dfs.append(df)
        print(f"Loaded: {f} ({len(df)} rows)")
    if dfs:
        big = pd.concat(dfs, ignore_index=True, sort=False)
    else:
        big = pd.DataFrame()
    return big


def consolidate_and_flag(big: pd.DataFrame):
    if big.empty:
        print("Nenhum dado carregado.")
        return pd.DataFrame()

    # create a sample_text by concatenating string columns
    text_cols = [c for c in big.columns if big[c].dtype == object]
    # exclude __source from sample_text concatenation
    text_cols = [c for c in text_cols if c != "__source"]

    def make_sample_text(row):
        parts = []
        for c in text_cols:
            v = row.get(c)
            if pd.isna(v):
                continue
            s = str(v).strip()
            if s:
                parts.append(s)
        return " \n ".join(parts)

    big['numero_proc_norm'] = big.apply(lambda r: normalize_proc(r.get('numero_processo') or r.get('processo') or r.get('processo_num') or ''), axis=1)
    big['sample_text'] = big.apply(make_sample_text, axis=1)

    grouped = {}
    for idx, row in big.iterrows():
        key = row['numero_proc_norm'] or f"ROW_{idx}"
        entry = grouped.get(key, {"numero_processo": row.get('numero_processo',''), "sample_text": [], "sources": set(), "itau": False, "veic": False})
        txt = row.get('sample_text','') or ''
        entry['sample_text'].append(txt)
        entry['sources'].add(row.get('__source',''))
        if text_has_any(txt, ITAU_PATTERNS):
            entry['itau'] = True
        if text_has_any(txt, VEIC_PATTERNS):
            entry['veic'] = True
        grouped[key] = entry

    rows = []
    for k, v in grouped.items():
        rows.append({
            'numero_processo': v.get('numero_processo') or k,
            'numero_proc_norm': k,
            'itau_flag': bool(v.get('itau', False)),
            'veiculos_flag': bool(v.get('veic', False)),
            'sample_text': '\n---\n'.join([s for s in v.get('sample_text') if s]),
            'sources': ','.join(sorted([s for s in v.get('sources') if s]))
        })

    out = pd.DataFrame(rows)
    return out


def main():
    big = load_csvs()
    out = consolidate_and_flag(big)
    os.makedirs('outputs', exist_ok=True)
    csv_path = 'outputs/consolidado_flags.csv'
    json_path = 'outputs/consolidado_flags.json'
    if not out.empty:
        out.to_csv(csv_path, index=False)
        out.to_json(json_path, orient='records', force_ascii=False)
        print(f"Outputs escritos em: {csv_path} e {json_path}")
    else:
        print('Nenhuma saída gerada.')


if __name__ == '__main__':
    main()
