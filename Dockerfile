FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV PYTHONUNBUFFERED=1
CMD ["python", "starter_scripts/01_pipeline_responder_14_questoes.py"]
