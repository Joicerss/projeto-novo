# Dockerfile para Projeto Jurimetria
FROM python:3.11-slim

# Metadados
LABEL maintainer="Projeto Jurimetria"
LABEL description="Container para análise jurimétrica de dados judiciais"
LABEL version="1.0.0"

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY . .

# Criar diretórios necessários
RUN mkdir -p data output notebooks

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expor porta para Jupyter (opcional)
EXPOSE 8888

# Comando padrão: executar análise completa
CMD ["python3", "jurimetria_completa.py"]

# Para executar Jupyter notebook ao invés da análise:
# docker run -p 8888:8888 jurimetria jupyter notebook --ip=0.0.0.0 --allow-root --no-browser
