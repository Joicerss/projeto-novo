# Projeto Novo - Pipeline de Classificação de Processos

Este repositório contém um pipeline completo para processamento e classificação de processos judiciais, incluindo validação de números CNJ, heurísticas configuráveis e geração de relatórios.

## Estrutura do Projeto

- `starter_scripts/`: Scripts principais do pipeline.
- `scripts/`: Scripts auxiliares (auto-preenchimento, geração de modelos).
- `tests/`: Testes unitários (validação CNJ, heurísticas, utils).
- `notebooks/`: Notebooks Jupyter para exploração e exemplos.
- `config/`: Exemplos de configuração.
- `outputs/`: Diretório onde os resultados são salvos.
- `data/`: Diretório para dados de entrada (ex: CSVs).

## Pré-requisitos

- Python 3.10+
- Docker (opcional, para execução em container)

## Uso Rápido (Makefile)

O projeto inclui um `Makefile` para facilitar as tarefas comuns:

```bash
# Instalar dependências
make install

# Executar testes (inclui validação CNJ)
make test

# Executar o pipeline completo localmente
make run

# Limpar outputs antigos
make clean
```

## Execução com Docker

Para garantir reprodutibilidade, você pode rodar tudo via Docker:

```bash
# Construir a imagem
make docker-build

# Executar o container (monta volumes data/ e outputs/)
make docker-run
```

## Validação CNJ

O projeto inclui um módulo de validação de números de processo no padrão CNJ (Conselho Nacional de Justiça).
Os testes de validação podem ser executados com:

```bash
pytest tests/test_cnj_validation.py
```

## Configuração de Heurísticas

O comportamento das heurísticas pode ser configurado via variável de ambiente `HEURISTICS_MODE` ou arquivo `heuristics.yml`.

Modos disponíveis:
- `strict` (padrão): Mais rigoroso na detecção (ex: exige valor monetário explícito para indenização).
- `lenient`: Mais permissivo (ex: aceita palavras-chave sem valor explícito).

Exemplo:
```bash
export HEURISTICS_MODE=lenient
make run
```

## CI/CD

O projeto possui um workflow de CI (`.github/workflows/docker-publish.yml`) configurado para:
1. Construir a imagem Docker.
2. Publicar no GitHub Container Registry (GHCR).
3. Executar um "smoke test" validando a imagem publicada.

*Nota: A execução do CI pode exigir aprovação manual na aba "Actions" do GitHub dependendo das configurações do repositório.*
