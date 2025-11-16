# Pipeline: uso rápido

Uso rápido (venv):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python starter_scripts/01_pipeline_responder_14_questoes.py
python starter_scripts/02_inspect_flags.py
python scripts/generate_modelo_respostas.py
```

Usando Docker:

```bash
docker build -t projeto-pipeline .
docker run --rm -v "$PWD":/app projeto-pipeline
```

Arquivos gerados:
- `outputs/consolidado_flags.csv` — consolidação com flags
- `outputs/flags_summary.csv` — estatísticas por flag
- `outputs/flags_inspection.xlsx` — amostra para revisão
- `outputs/modelo_respostas.xlsx` — planilha modelo com 14 perguntas
