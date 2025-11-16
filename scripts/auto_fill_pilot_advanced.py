"""
Preenchimento avançado (heurísticas) para os 30 processos do piloto.

Heurísticas adicionais implementadas (rascunho):
- detecta CNPJ/CPF
- detecta datas (dd/mm/yyyy, yyyy) e valores em R$
- flags para termos jurídicos (sentença, indenização, acidente, vítima, execução)
- preenche perguntas 1..9 quando aplicável e adiciona coluna `confidence` (0..1)

Gera: `outputs/pilot_30_filled_advanced.xlsx` e CSV correspondente.

Uso: python scripts/auto_fill_pilot_advanced.py
"""
import os
import json
import re
from pathlib import Path
import pandas as pd
try:
    import yaml
except Exception:
    yaml = None


RE_CNPJ = re.compile(r"\b(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{14})\b")
RE_CPF = re.compile(r"\b(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})\b")
RE_DATE = re.compile(r"\b(\d{2}/\d{2}/\d{4})\b")
RE_YEAR = re.compile(r"\b(19|20)\d{2}\b")
RE_VALOR = re.compile(r"R\$\s?[\d\.]+(?:,\d{2})?")


KEYS_SENTENCA = ["sentença", "acórdão", "decisão", "julg", "conden"]
KEYS_INDEMN = ["indeniz", "indenização", "indeniza", "indenizado", "indenizar"]
KEYS_ACIDENTE = ["acident", "colis", "batida", "acidente de trânsito", "capot"]
KEYS_VITIMA = ["vítim", "vitim", "ferid", "morto", "óbito", "morte"]
KEYS_EXEC = ["execução", "penhora", "arresto", "bloqueio", "protesto", "cobrança"]


def extract_first(regex, text):
    m = regex.search(text)
    return m.group(0) if m else ''


def contains_any(text, keywords):
    t = text.lower()
    return any(k in t for k in keywords)


def score_matches(matches):
    # simple score: fraction of True matches
    if not matches:
        return 0.0
    return sum(1 for v in matches if v) / len(matches)


def fill_advanced(row):
    txt = str(row.get('sample_text','') or '').lower()
    filled = {}
    # pergunta_1 and _2 kept from base heuristics if present
    itau = str(row.get('itau_flag','')).lower() in ('true','1','sim','yes','y','t')
    veic = str(row.get('veiculos_flag','')).lower() in ('true','1','sim','yes','y','t')
    filled['pergunta_1'] = 'sim' if itau else 'nao'
    filled['pergunta_2'] = 'sim' if veic else 'nao'

    # pergunta_3: presença de sentença/decisão
    p3 = contains_any(txt, KEYS_SENTENCA)
    filled['pergunta_3'] = 'sim' if p3 else 'nao'

    # pergunta_4: comportamento configurável via HEURISTICS_MODE
    # Ordem de resolução (do mais prioritário ao menos):
    # 1. Variável de ambiente `HEURISTICS_MODE`
    # 2. Arquivo de configuração `heuristics.yml` / `heuristics.yaml` / `heuristics.json` com chave `mode`
    # 3. Padrão: 'strict'
    def get_heuristics_mode():
        # 1) env
        env_mode = os.getenv('HEURISTICS_MODE')
        if env_mode:
            return env_mode.lower()
        # 2) file in repo root
        repo_root = Path(__file__).resolve().parents[1]
        y_paths = [repo_root / 'heuristics.yml', repo_root / 'heuristics.yaml']
        j_path = repo_root / 'heuristics.json'
        for p in y_paths:
            if p.exists() and yaml is not None:
                try:
                    cfg = yaml.safe_load(p.read_text()) or {}
                    m = cfg.get('mode') or cfg.get('HEURISTICS_MODE') or cfg.get('heuristics_mode')
                    if m:
                        return str(m).lower()
                except Exception:
                    continue
        if j_path.exists():
            try:
                cfg = json.loads(j_path.read_text())
                m = cfg.get('mode') or cfg.get('HEURISTICS_MODE') or cfg.get('heuristics_mode')
                if m:
                    return str(m).lower()
            except Exception:
                pass
        return 'strict'

    mode = get_heuristics_mode()
    if mode == 'lenient':
        p4 = contains_any(txt, KEYS_INDEMN) or bool(RE_VALOR.search(txt))
    else:
        p4 = bool(RE_VALOR.search(txt))
    filled['pergunta_4'] = 'sim' if p4 else 'nao'

    # pergunta_5: extrair CNPJ/CPF se houver
    cnpj = extract_first(RE_CNPJ, txt)
    cpf = extract_first(RE_CPF, txt)
    filled['pergunta_5'] = cnpj or cpf or ''

    # pergunta_6: extrair primeira data ou ano
    date = extract_first(RE_DATE, txt)
    year = extract_first(RE_YEAR, txt)
    filled['pergunta_6'] = date or year or ''

    # pergunta_7: acidente
    p7 = contains_any(txt, KEYS_ACIDENTE)
    filled['pergunta_7'] = 'sim' if p7 else 'nao'

    # pergunta_8: vítima/óbito
    p8 = contains_any(txt, KEYS_VITIMA)
    filled['pergunta_8'] = 'sim' if p8 else 'nao'

    # pergunta_9: execução/penhora
    p9 = contains_any(txt, KEYS_EXEC)
    filled['pergunta_9'] = 'sim' if p9 else 'nao'

    # perguntas 10-14: mantêm em branco
    for i in range(10,15):
        filled[f'pergunta_{i}'] = ''

    # evidencias: first 800 chars
    evid = (txt[:800] + '...') if len(txt) > 800 else txt
    filled['evidencias'] = evid

    # confidence: based on matches
    matches = [itau, veic, p3, p4, bool(cnpj or cpf), bool(date or year), p7, p8, p9]
    filled['confidence'] = round(score_matches(matches), 2)

    # numero_processo
    num = row.get('numero_processo') or row.get('numero_proc_norm') or ''
    filled['numero_processo'] = num
    return filled


def main():
    p_pilot = Path('outputs/pilot_30.csv')
    if not p_pilot.exists():
        print('Arquivo pilot_30.csv não encontrado. Rode o pipeline e gere o piloto primeiro.')
        return
    pilot = pd.read_csv(p_pilot, dtype=str)
    rows = []
    for _, r in pilot.iterrows():
        rows.append(fill_advanced(r))
    df = pd.DataFrame(rows)
    out_xlsx = Path('outputs/pilot_30_filled_advanced.xlsx')
    out_csv = Path('outputs/pilot_30_filled_advanced.csv')
    df.to_excel(out_xlsx, index=False)
    df.to_csv(out_csv, index=False)
    print(f'Preenchimento avançado salvo: {out_xlsx} (linhas={len(df)})')


if __name__ == '__main__':
    main()
