# Curso Prático de Jurimetria com Docker 📊⚖️

Bem-vindo ao curso prático de jurimetria focado em **recuperação judicial**. Este projeto oferece um ambiente reproduzível usando Docker para aprender análise de dados jurídicos passo a passo.

## 🎯 Objetivo

Este curso ensina como:
- Consolidar e processar dados de processos judiciais
- Identificar padrões em recuperações judiciais usando heurísticas
- Analisar dados jurídicos com Python e bibliotecas de ciência de dados
- Responder às 14 questões fundamentais sobre recuperação judicial
- Desenvolver habilidades de cientista de dados jurídicos

## 📁 Estrutura do Projeto

```
projeto-novo/
├── starter_scripts/          # Scripts do pipeline de análise
│   └── 01_pipeline_responder_14_questoes.py
├── data/                     # Dados de entrada (CSVs)
├── outputs/                  # Resultados gerados
├── notebooks/                # Jupyter notebooks interativos
├── Dockerfile               # Configuração do ambiente Docker
├── docker-compose.yml       # Orquestração do container
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## 🚀 Início Rápido com Docker

### Pré-requisitos

- [Docker](https://www.docker.com/get-started) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado
- Git (opcional, para clonar o repositório)

### Passo 1: Construir o Container

```bash
docker-compose build
```

Este comando irá:
- Criar uma imagem Docker com Python 3.11
- Instalar todas as dependências (pandas, jupyter, playwright, tesseract, etc.)
- Configurar o ambiente Playwright para web scraping

**Tempo estimado:** 5-10 minutos (na primeira vez)

### Passo 2: Iniciar o Container

```bash
docker-compose up --detach
```

O container estará rodando em segundo plano (modo detached).

### Passo 3: Acessar o Container

```bash
docker exec -it jurimetria-course bash
```

Agora você está dentro do container com o ambiente configurado! 🎉

## 📊 Executando o Pipeline

### Pipeline 01: Consolidação de CSVs e Flags

Este script consolida arquivos CSV de processos e gera flags baseadas em heurísticas.

```bash
python starter_scripts/01_pipeline_responder_14_questoes.py
```

**Entrada:** Arquivos CSV em `data/` (ou gera dados de exemplo se não houver)

**Saída:**
- `outputs/consolidado_flags.csv` - Dataset consolidado com flags
- `outputs/consolidado_flags.json` - Mesmos dados em formato JSON

**Flags geradas:**
- `tem_recurso`, `tem_agravo`, `tem_apelacao`, `tem_embargos`
- `tem_liminar`, `tem_decisao_monocrática`, `tem_sentenca`, `tem_acordao`
- `processo_ativo`, `processo_arquivado`, `processo_suspenso`
- `valor_causa_alto`, `valor_causa_baixo`
- `tempo_tramitacao_longo`

### Visualizando os Resultados

```bash
# Ver primeiras linhas do CSV gerado
head -n 20 outputs/consolidado_flags.csv

# Ver estatísticas
python -c "import pandas as pd; df = pd.read_csv('outputs/consolidado_flags.csv'); print(df.describe())"
```

## 📓 Jupyter Notebook (Análise Interativa)

Para explorar os dados de forma interativa:

```bash
# Dentro do container
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

Depois acesse no seu navegador: `http://localhost:8888`

O token de acesso será exibido no terminal.

## 📦 Adicionando Seus Dados

1. Coloque seus arquivos CSV na pasta `data/`
2. Os CSVs devem conter (idealmente) estas colunas:
   - `numero_processo` - Número do processo
   - `classe` - Classe processual
   - `assunto` - Assunto do processo
   - `data_distribuicao` - Data de distribuição
   - `valor_causa` - Valor da causa
   - `situacao` - Situação atual
   - `movimentacoes` - Movimentações processuais

3. Execute o pipeline novamente

## 🛠️ Comandos Úteis Docker

```bash
# Parar o container
docker-compose down

# Ver logs do container
docker-compose logs -f

# Reiniciar o container
docker-compose restart

# Reconstruir após mudanças no Dockerfile
docker-compose build --no-cache

# Listar containers rodando
docker ps
```

## 📚 Dependências Principais

- **pandas** - Manipulação de dados
- **numpy** - Computação numérica  
- **jupyter** - Notebooks interativos
- **matplotlib/seaborn** - Visualização
- **scikit-learn** - Machine learning
- **lifelines** - Análise de sobrevivência (Kaplan-Meier, Cox)
- **playwright** - Web scraping
- **pytesseract** - OCR para PDFs

## 🎓 As 14 Questões sobre Recuperação Judicial

Este curso ajuda a responder questões como:

1. Qual a taxa de aprovação de planos de recuperação?
2. Quanto tempo leva em média para aprovar um plano?
3. Quais são os principais credores?
4. Qual o perfil das empresas em recuperação?
5. Há diferenças regionais nos resultados?
... e mais 9 questões específicas do caso

## 🐛 Solução de Problemas

### Erro de permissão ao executar scripts

```bash
chmod +x starter_scripts/*.py
```

### Container não inicia

Verifique se as portas estão disponíveis:
```bash
lsof -i :8888
```

### Falta de espaço em disco

Limpe containers e imagens antigas:
```bash
docker system prune -a
```

## 📄 Licença

Este projeto é fornecido para fins educacionais.

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, abra uma issue ou pull request.

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.

---

**Desenvolvido para cientistas de dados jurídicos** 👨‍💻⚖️

*Última atualização: 2025*
