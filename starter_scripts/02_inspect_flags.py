"""
Inspeção e exportação dos resultados consolidados (flags).
Gera:
 - outputs/flags_summary.csv  (estatísticas por flag)
 - outputs/flags_inspection.xlsx (planilha com amostra e colunas relevantes)

Usage: python starter_scripts/02_inspect_flags.py
"""
import os
import pandas as pd


def load_consolidado(path="outputs/consolidado_flags.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    df = pd.read_csv(path, dtype=str)
    return df


def summarize_flags(df):
    # Detect boolean-like columns (itau_flag, veiculos_flag etc.)
    possible_flags = [c for c in df.columns if c.endswith("_flag") or c in ("itau_flag", "veiculos_flag")]
    summary = []
    for f in possible_flags:
        series = df[f].fillna("False").astype(str)
        total = len(series)
        true_count = series.str.lower().isin(["true","1","t","y","yes"]).sum()
        summary.append({"flag": f, "total": total, "true_count": int(true_count), "true_pct": float(true_count)/max(1,total)})
    return pd.DataFrame(summary)


def export_inspection(df, out_xlsx="outputs/flags_inspection.xlsx", sample_n=500):
    os.makedirs(os.path.dirname(out_xlsx), exist_ok=True)
    # pick flagged rows first, then random sample to reach sample_n
    flags = [c for c in df.columns if c.endswith("_flag")]
    if flags:
        mask = pd.Series(False, index=df.index)
        for f in flags:
            mask = mask | df[f].fillna(False).astype(str).str.lower().isin(["true","1","t","y","yes"]) 
        flagged = df[mask]
    else:
        flagged = df.iloc[0:0]

    remaining = df[~df.index.isin(flagged.index)].sample(n=max(0, sample_n - len(flagged)), random_state=42) if len(df) > len(flagged) else df.iloc[0:0]
    out = pd.concat([flagged, remaining])

    # columns to keep
    keep = ["numero_processo", "itau_flag", "veiculos_flag", "sample_text", "sources"]
    keep = [c for c in keep if c in out.columns]
    with pd.ExcelWriter(out_xlsx) as writer:
        out[keep].to_excel(writer, index=False, sheet_name="inspection")
    print(f"Inspection exported to: {out_xlsx} (rows={len(out)})")


def main():
    try:
        df = load_consolidado()
    except FileNotFoundError as e:
        print(e)
        return
    summary = summarize_flags(df)
    os.makedirs("outputs", exist_ok=True)
    summary.to_csv("outputs/flags_summary.csv", index=False)
    print("Flag summary written to: outputs/flags_summary.csv")
    export_inspection(df)


if __name__ == "__main__":
    main()
