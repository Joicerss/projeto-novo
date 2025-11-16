# Pacote de Extração DataJud/CNJ - Projeto Jurimetria

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Pacote completo para extração, validação e análise de dados de processos judiciais do sistema DataJud/CNJ.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Características](#características)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Os 14 Campos CNJ](#os-14-campos-cnj)
- [Exemplos](#exemplos)
- [Docker](#docker)
- [Testes e Validação](#testes-e-validação)
- [Resolução de Problemas](#resolução-de-problemas)
- [Contribuindo](#contribuindo)

## 🎯 Visão Geral

Este pacote fornece ferramentas completas para:

1. **Extração de dados** de processos judiciais via API DataJud/CNJ
2. **Validação** de números de processos no formato CNJ
3. **Análise jurimetrica** dos dados extraídos
4. **Geração de relatórios** automáticos em múltiplos formatos

O pacote foi desenvolvido seguindo os padrões estabelecidos pelo Conselho Nacional de Justiça (CNJ) e pela Resolução CNJ nº 65/2008.

## ✨ Características

- ✅ Validação automática de números de processos (formato CNJ)
- ✅ Extração estruturada dos 14 campos principais definidos pelo CNJ
- ✅ Suporte a proxy para ambientes corporativos
- ✅ Processamento em lote de múltiplos processos
- ✅ Geração de logs detalhados
- ✅ Exportação para Excel e CSV
- ✅ Notebook Jupyter com exemplos práticos
- ✅ Containerização com Docker
- ✅ Planilha modelo para organização de dados

## 📁 Estrutura do Projeto

```
projeto-novo/
├── extrair_datajud.py          # Script principal de extração
├── validacao_cnj.py            # Script de validação de números CNJ
├── exemplo_extracao.ipynb      # Notebook Jupyter com exemplos
├── planilha_modelo.xlsx        # Planilha modelo (14 campos CNJ)
├── requirements.txt            # Dependências Python
├── Dockerfile                  # Container Docker
├── .env.exemplo                # Exemplo de configuração
├── README_PACOTE.md           # Este arquivo
├── dados/                      # Diretório para dados brutos
├── resultados/                 # Diretório para resultados processados
└── logs/                       # Diretório para arquivos de log
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Credenciais de acesso à API DataJud/CNJ

### Instalação Local

1. **Clone ou baixe este repositório**

```bash
git clone https://github.com/Joicerss/projeto-novo.git
cd projeto-novo
```

2. **Crie um ambiente virtual (recomendado)**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Configurar Credenciais

Copie o arquivo `.env.exemplo` para `.env`:

```bash
cp .env.exemplo .env
```

Edite o arquivo `.env` com suas credenciais:

```ini
# API DataJud/CNJ
DATAJUD_API_KEY=sua_chave_api_aqui
DATAJUD_BASE_URL=https://api-publica.datajud.cnj.jus.br

# Configuração de Proxy (opcional)
USE_PROXY=false
PROXY_URL=http://proxy.example.com:8080

# Número de processos para teste
N_PILOTOS=5
```

### 2. Obter Chave de API

Para obter acesso à API DataJud:

1. Acesse o portal do CNJ: https://www.cnj.jus.br
2. Solicite credenciais de acesso ao DataJud
3. Siga o processo de cadastro e autorização
4. Adicione a chave recebida no arquivo `.env`

**IMPORTANTE**: Mantenha suas credenciais seguras e nunca as compartilhe ou comite no Git.

## 💻 Uso

### Validação de Números de Processos

Execute a validação CNJ para verificar se os números estão no formato correto:

```bash
python validacao_cnj.py
```

Este script irá:
- Validar o formato dos números de processo
- Verificar dígitos verificadores
- Extrair componentes (tribunal, vara, etc.)
- Gerar relatório de validação

### Extração de Dados

Execute o script de extração para buscar dados de processos:

```bash
python extrair_datajud.py
```

O script irá:
- Conectar à API DataJud
- Buscar informações dos processos
- Extrair os 14 campos padronizados
- Salvar resultados em Excel

### Usando o Notebook Jupyter

Para uma experiência interativa:

```bash
jupyter notebook exemplo_extracao.ipynb
```

O notebook contém:
- Exemplos passo a passo
- Visualizações de dados
- Análises estatísticas
- Fluxo completo com 5 processos-piloto

## 📊 Os 14 Campos CNJ

O pacote extrai os seguintes campos padronizados conforme CNJ:

| # | Campo | Descrição |
|---|-------|-----------|
| 1 | Número do Processo | Número único no formato CNJ |
| 2 | Classe Processual | Tipo de ação judicial |
| 3 | Assunto | Área do direito e tema |
| 4 | Data de Ajuizamento | Data de início do processo |
| 5 | Órgão Julgador | Vara ou instância responsável |
| 6 | Magistrado | Nome do juiz responsável |
| 7 | Valor da Causa | Valor monetário da ação |
| 8 | Partes - Polo Ativo | Autor(es) da ação |
| 9 | Partes - Polo Passivo | Réu(s) da ação |
| 10 | Movimentações | Histórico de eventos |
| 11 | Data da Última Movimentação | Último evento registrado |
| 12 | Situação do Processo | Status atual |
| 13 | Data do Trânsito em Julgado | Data sem possibilidade de recurso |
| 14 | Resultado | Desfecho do processo |

### Formato de Número CNJ

O número do processo segue o formato: **NNNNNNN-DD.AAAA.J.TR.OOOO**

Onde:
- **NNNNNNN**: Número sequencial (7 dígitos)
- **DD**: Dígito verificador (2 dígitos)
- **AAAA**: Ano do ajuizamento (4 dígitos)
- **J**: Segmento da justiça (1 dígito)
- **TR**: Tribunal (2 dígitos)
- **OOOO**: Vara de origem (4 dígitos)

Exemplo: `0000001-01.2024.8.00.0001`

## 📝 Exemplos

### Exemplo 1: Validar um único processo

```python
from validacao_cnj import ValidadorCNJ

numero = "0000001-01.2024.8.00.0001"
valido, mensagem = ValidadorCNJ.validar_formato(numero)

if valido:
    print(f"✓ Processo válido: {numero}")
    componentes = ValidadorCNJ.extrair_componentes(numero)
    print(f"  Ano: {componentes['ano_ajuizamento']}")
    print(f"  Tribunal: {componentes['tribunal']}")
else:
    print(f"✗ Processo inválido: {mensagem}")
```

### Exemplo 2: Extrair dados de múltiplos processos

```python
from extrair_datajud import DataJudExtractor

# Inicializar extrator
extractor = DataJudExtractor()

# Lista de processos
processos = [
    "0000001-01.2024.8.00.0001",
    "0000002-01.2024.8.00.0001",
    "0000003-01.2024.8.00.0001"
]

# Processar lote
df_resultados = extractor.processar_lote(processos)

# Salvar resultados
df_resultados.to_excel("resultados/extracao.xlsx", index=False)
print(f"Extraídos {len(df_resultados)} processos")
```

### Exemplo 3: Validar arquivo Excel

```python
from validacao_cnj import validar_arquivo

# Validar planilha com números de processos
df_validacao = validar_arquivo(
    "planilha_modelo.xlsx",
    coluna_numero="1. Número do Processo"
)

# Ver estatísticas
print(df_validacao['valido'].value_counts())
```

## 🐳 Docker

### Construir a imagem

```bash
docker build -t datajud-extractor .
```

### Executar container

```bash
docker run -p 8888:8888 -v $(pwd)/dados:/app/dados -v $(pwd)/resultados:/app/resultados datajud-extractor
```

Acesse o Jupyter no navegador: `http://localhost:8888`

### Docker Compose (opcional)

Crie um arquivo `docker-compose.yml`:

```yaml
version: '3.8'
services:
  jupyter:
    build: .
    ports:
      - "8888:8888"
    volumes:
      - ./dados:/app/dados
      - ./resultados:/app/resultados
      - ./logs:/app/logs
    environment:
      - DATAJUD_API_KEY=${DATAJUD_API_KEY}
```

Execute:

```bash
docker-compose up
```

## 🧪 Testes e Validação

### Executar Teste de Validação CNJ

```bash
python validacao_cnj.py
```

Este script executa testes automáticos com casos válidos e inválidos.

### Executar com Processos Piloto

O notebook `exemplo_extracao.ipynb` já vem configurado com 5 processos-piloto para teste.

### Verificar Logs

Todos os logs são salvos em `logs/extracao.log`. Para monitorar em tempo real:

```bash
# Linux/Mac
tail -f logs/extracao.log

# Windows
Get-Content logs/extracao.log -Wait
```

## 🔧 Resolução de Problemas

### Erro de Autenticação

**Problema**: `401 Unauthorized` ou `403 Forbidden`

**Solução**:
- Verifique se a chave API está correta no arquivo `.env`
- Confirme se as credenciais estão ativas
- Verifique se há restrições de IP

### Erro de Conexão

**Problema**: `Connection timeout` ou `Connection refused`

**Solução**:
- Verifique sua conexão com a internet
- Se estiver atrás de um firewall/proxy, configure `USE_PROXY=true` no `.env`
- Verifique se a URL da API está correta

### Número de Processo Inválido

**Problema**: Script rejeita número de processo

**Solução**:
- Verifique o formato: NNNNNNN-DD.AAAA.J.TR.OOOO
- Use o script `validacao_cnj.py` para identificar o erro
- Corrija o dígito verificador se necessário

### Dependências Faltando

**Problema**: `ModuleNotFoundError`

**Solução**:
```bash
pip install -r requirements.txt --upgrade
```

## 📚 Documentação Adicional

### API DataJud

- [Portal CNJ](https://www.cnj.jus.br)
- [Documentação DataJud](https://www.cnj.jus.br/sistemas/datajud/)
- [Resolução CNJ nº 65/2008](https://atos.cnj.jus.br/atos/detalhar/119) - Numeração Única

### Jurimetria

- [Jurimetria - Conceitos](https://abj.org.br/o-que-e-jurimetria/)
- [Análise de Dados Jurídicos](https://observatorioitajuba.com.br/)

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas e suporte:

- Abra uma [issue](https://github.com/Joicerss/projeto-novo/issues) no GitHub
- Consulte a documentação do CNJ
- Entre em contato com o time de desenvolvimento

## 🎓 Citação

Se você usar este pacote em trabalhos acadêmicos, por favor cite:

```
Projeto Jurimetria - Pacote de Extração DataJud/CNJ
Disponível em: https://github.com/Joicerss/projeto-novo
```

---

**Desenvolvido para facilitar a análise jurimetrica e pesquisa empírica no Direito.**

**Versão**: 1.0.0  
**Data**: Novembro 2025  
**Status**: ✅ Pronto para uso
