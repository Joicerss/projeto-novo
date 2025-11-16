# 🚀 Guia Rápido - Início Imediato

Este guia ajuda você a começar a usar o pacote DataJud/CNJ em menos de 5 minutos.

## ⚡ Início Rápido (3 passos)

### 1️⃣ Instalar Dependências

```bash
# Linux/Mac
pip3 install -r requirements.txt

# Windows
pip install -r requirements.txt
```

### 2️⃣ Configurar Credenciais

```bash
# Copiar arquivo de exemplo
cp .env.exemplo .env

# Editar e adicionar sua chave API
# DATAJUD_API_KEY=sua_chave_aqui
```

### 3️⃣ Executar

**Opção A: Script Automático**

```bash
# Linux/Mac
./executar.sh

# Windows
executar.bat
```

**Opção B: Manual**

```bash
# Validar números CNJ
python validacao_cnj.py

# Extrair dados
python extrair_datajud.py

# Jupyter Notebook
jupyter notebook exemplo_extracao.ipynb
```

## 🐳 Usando Docker (Alternativa)

```bash
# Construir imagem
docker build -t datajud-extractor .

# Executar
docker run -p 8888:8888 -v $(pwd)/resultados:/app/resultados datajud-extractor
```

Acesse: http://localhost:8888

## 📊 Usar a Planilha Modelo

1. Abra `planilha_modelo.xlsx`
2. Veja os 5 exemplos de processos
3. Substitua pelos seus dados reais
4. Use para validação: `python validacao_cnj.py`

## 📝 Fluxo Completo de Uso

```
1. Validar números → validacao_cnj.py
2. Extrair dados → extrair_datajud.py
3. Analisar → exemplo_extracao.ipynb
4. Resultados → pasta resultados/
```

## 🔑 Onde Obter a Chave API

1. Acesse: https://www.cnj.jus.br
2. Vá para a seção DataJud
3. Solicite credenciais de acesso
4. Aguarde aprovação
5. Adicione a chave no arquivo `.env`

## ❓ Problemas Comuns

### Python não encontrado
```bash
# Verificar instalação
python --version
# ou
python3 --version
```

### Módulos faltando
```bash
pip install -r requirements.txt --upgrade
```

### Erro de autenticação
- Verifique se a chave API está correta no `.env`
- Confirme se as credenciais estão ativas

## 📚 Próximos Passos

- Leia o [README_PACOTE.md](README_PACOTE.md) completo
- Explore o notebook [exemplo_extracao.ipynb](exemplo_extracao.ipynb)
- Veja os 14 campos CNJ na documentação

## 💡 Dica Pro

Use o modo demonstração sem API:

```python
# No arquivo extrair_datajud.py
# Comente a linha de extração real:
# df_resultados = extractor.processar_lote(processos_exemplo)

# E use os dados de exemplo já presentes no código
```

## 🎯 Teste Rápido

Execute este comando para testar tudo:

```bash
# Linux/Mac
./executar.sh

# Windows
executar.bat

# Escolha opção 4 (Executar todos os testes)
```

---

**Pronto! Você está preparado para começar. 🎉**

Para documentação completa, consulte [README_PACOTE.md](README_PACOTE.md)
