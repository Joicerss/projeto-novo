# Makefile para Projeto Novo - Pipeline de Classificação de Processos

PYTHON := python3
PIP := pip
DOCKER := docker
IMAGE_NAME := projeto-novo-pipeline

.PHONY: all install test run clean docker-build docker-run

all: install test run

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) -m pytest tests/

run:
	$(PYTHON) starter_scripts/01_pipeline_responder_14_questoes.py
	$(PYTHON) scripts/auto_fill_pilot_advanced.py

clean:
	rm -rf outputs/*
	rm -rf __pycache__
	rm -rf */__pycache__

docker-build:
	$(DOCKER) build -t $(IMAGE_NAME) .

docker-run:
	mkdir -p outputs
	$(DOCKER) run --rm -v $(PWD)/data:/app/data -v $(PWD)/outputs:/app/outputs $(IMAGE_NAME)

help:
	@echo "Comandos disponíveis:"
	@echo "  make install       - Instala dependências"
	@echo "  make test          - Executa testes unitários"
	@echo "  make run           - Executa o pipeline localmente"
	@echo "  make clean         - Limpa arquivos temporários e outputs"
	@echo "  make docker-build  - Constrói a imagem Docker"
	@echo "  make docker-run    - Executa o pipeline via Docker"
