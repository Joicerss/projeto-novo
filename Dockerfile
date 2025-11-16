# Dockerfile for Jurimetry Course
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Playwright, Tesseract, and other tools
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    wget \
    gnupg \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p data outputs notebooks

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV JUPYTER_ENABLE_LAB=yes

# Expose Jupyter port
EXPOSE 8888

# Default command (can be overridden in docker-compose)
CMD ["bash"]
