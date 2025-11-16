# 🚀 Guia de Início Rápido - Curso de Jurimetria

Este guia mostra os comandos essenciais para começar rapidamente.

## Pré-requisitos

✅ Docker instalado ([Baixar aqui](https://www.docker.com/get-started))

## Comandos Rápidos

### 1️⃣ Construir o ambiente Docker (primeira vez)

```bash
docker compose build
```

⏱️ **Tempo:** ~5-10 minutos na primeira vez

---

### 2️⃣ Iniciar o container

```bash
docker compose up -d
```

✅ Container rodando em segundo plano!

---

### 3️⃣ Entrar no container

```bash
docker exec -it jurimetria-course bash
```

🎉 Agora você está dentro do ambiente configurado!

---

### 4️⃣ Executar o pipeline de análise

```bash
python starter_scripts/01_pipeline_responder_14_questoes.py
```

📊 **Resultado:** Arquivos gerados em `outputs/`
- `consolidado_flags.csv`
- `consolidado_flags.json`

---

### 5️⃣ Visualizar resultados

```bash
# Ver primeiras linhas do CSV
head outputs/consolidado_flags.csv

# Ver estatísticas
cat outputs/consolidado_flags.json | python -m json.tool | head -40
```

---

### 6️⃣ Iniciar Jupyter Notebook (opcional)

```bash
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

📓 Acesse: `http://localhost:8888` (token será mostrado no terminal)

---

### 7️⃣ Parar o container

```bash
# Sair do container (se estiver dentro)
exit

# Parar o container
docker compose down
```

---

## 🎓 Próximos Passos

1. **Adicionar seus dados:** Coloque arquivos CSV em `data/`
2. **Executar pipeline novamente:** Com seus dados reais
3. **Explorar notebook:** `notebooks/01_analise_exploratoria.ipynb`
4. **Personalizar análises:** Modificar flags e heurísticas

---

## ⚠️ Solução de Problemas

### Container não inicia

```bash
# Verificar portas em uso
docker ps

# Limpar containers antigos
docker system prune
```

### Erro "permission denied"

```bash
# Tornar scripts executáveis
chmod +x starter_scripts/*.py
```

### Comando não encontrado

Se `docker compose` não funcionar, tente:
```bash
docker-compose build  # Para Docker Compose v1
```

---

## 📚 Documentação Completa

Veja `README.md` para informações detalhadas sobre:
- Estrutura do projeto
- Flags disponíveis
- Dependências instaladas
- As 14 questões de jurimetria

---

**Bons estudos!** 🎯⚖️
