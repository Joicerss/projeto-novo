"""
Gera uma planilha Excel de modelo (`modelo_respostas.xlsx`) com colunas para revisão.
Run: python scripts/generate_modelo_respostas.py
"""
import os
import pandas as pd


def generate(path="outputs/modelo_respostas.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cols = [
        "numero_processo",
        "pergunta_1",
        "pergunta_2",
        "pergunta_3",
        "pergunta_4",
        "pergunta_5",
        "pergunta_6",
        "pergunta_7",
        "pergunta_8",
        "pergunta_9",
        "pergunta_10",
        "pergunta_11",
        "pergunta_12",
        "pergunta_13",
        "pergunta_14",
        "evidencias"
    ]
    df = pd.DataFrame(columns=cols)
    df.to_excel(path, index=False)
    print(f"Modelo gerado em: {path}")


if __name__ == "__main__":
    generate()
