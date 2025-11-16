# Formato de Dados - Curso de Jurimetria

Este documento descreve o formato esperado dos arquivos CSV para o curso.

## 📋 Estrutura dos Dados

Os arquivos CSV devem estar na pasta `data/` e conter as seguintes colunas:

### Colunas Principais

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| `numero_processo` | String | Número do processo judicial | `0001234-56.2023.8.26.0100` |
| `classe` | String | Classe processual | `Recuperação Judicial` |
| `assunto` | String | Assunto do processo | `Plano de Recuperação Judicial` |
| `data_distribuicao` | String/Date | Data de distribuição do processo | `2023-01-15` ou `15/01/2023` |
| `valor_causa` | Float | Valor da causa em reais | `5000000.00` |
| `situacao` | String | Situação atual do processo | `Em andamento`, `Ativo`, `Arquivado` |
| `movimentacoes` | String | Movimentações processuais (separadas por ponto-e-vírgula) | `Distribuição; Liminar deferida; Sentença` |

### Colunas Opcionais

Você pode adicionar outras colunas relevantes:

- `juiz` - Nome do juiz responsável
- `comarca` - Comarca onde tramita
- `vara` - Vara judicial
- `polo_ativo` - Requerente/autor
- `polo_passivo` - Requerido/réu
- `advogado_autor` - Advogado da parte autora
- `data_sentenca` - Data da sentença (se houver)
- `resultado` - Resultado final (se houver)

## 📝 Exemplo de CSV

```csv
numero_processo,classe,assunto,data_distribuicao,valor_causa,situacao,movimentacoes
0001234-56.2023.8.26.0100,Recuperação Judicial,Recuperação Judicial,2023-01-15,5000000.00,Em andamento,"Distribuição; Liminar deferida; Sentença proferida"
0009876-54.2023.8.26.0200,Recuperação Judicial,Plano de Recuperação,2023-03-20,850000.00,Ativo,"Distribuição; Decisão monocrática"
0005555-11.2022.8.26.0300,Recuperação Judicial,Aprovação de Plano,2022-06-10,12000000.00,Sentenciado,"Distribuição; Audiência; Sentença; Recurso"
```

## 🎯 Palavras-Chave para Detecção de Flags

O pipeline identifica flags automaticamente baseado em palavras-chave:

### Recursos
- `recurso`, `agravo`, `apelação`, `apelacao`, `embargo`

### Decisões
- `liminar`, `decisão monocrática`, `decisao monocratica`, `sentença`, `sentenca`, `acórdão`, `acordao`

### Situações
- **Ativo:** `ativo`, `andamento`
- **Arquivado:** `arquivado`, `baixado`
- **Suspenso:** `suspenso`, `sobrestado`

### Valores
- **Alto:** > R$ 1.000.000,00
- **Baixo:** < R$ 100.000,00

### Tempo
- **Tramitação Longa:** > 730 dias (2 anos)

## 💡 Dicas

1. **Use ponto-e-vírgula (;)** para separar múltiplas movimentações
2. **Formato de data:** Preferencialmente `YYYY-MM-DD` ou `DD/MM/YYYY`
3. **Valor numérico:** Use ponto como separador decimal
4. **Texto livre:** Coloque entre aspas duplas se contiver vírgulas ou ponto-e-vírgula

## 🔍 Como Coletar Dados

### Fontes Possíveis

1. **Tribunais de Justiça (TJs)**
   - Consulta processual online
   - Web scraping com Playwright (incluído no curso)

2. **DataJud (CNJ)**
   - API oficial do Conselho Nacional de Justiça
   - Dados estruturados de processos

3. **Diários Oficiais**
   - Publicações de decisões e movimentações

4. **Exportação Manual**
   - Alguns tribunais permitem exportar consultas em CSV/Excel

### Web Scraping (Avançado)

O curso inclui ferramentas para web scraping:
- **Playwright** - Automação de navegadores
- **BeautifulSoup** - Parsing de HTML
- **Tesseract OCR** - Extração de texto de PDFs/imagens

## 📂 Organização dos Arquivos

Recomendações:

```
data/
├── tj_sp_recuperacao_judicial_2023.csv
├── tj_rj_recuperacao_judicial_2023.csv
├── cnj_datajud_recuperacao_2022_2023.csv
└── README.txt  (descrição dos arquivos)
```

## ✅ Validação dos Dados

Após colocar os arquivos em `data/`, execute:

```bash
python starter_scripts/01_pipeline_responder_14_questoes.py
```

O script irá:
- ✅ Validar as colunas
- ✅ Normalizar números de processo
- ✅ Gerar flags automaticamente
- ✅ Criar arquivo consolidado em `outputs/`

## 🆘 Suporte

Se seus dados estão em formato diferente:
1. Renomeie as colunas para corresponder ao padrão
2. Converta datas para formato padrão
3. Ajuste o script `01_pipeline_responder_14_questoes.py` se necessário

---

**Nota:** Se você não tem dados próprios, o pipeline gera automaticamente um dataset de exemplo para você começar a aprender! 🎓
