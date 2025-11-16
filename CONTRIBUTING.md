# Guia de Contribuição

Obrigado por considerar contribuir para o Projeto Jurimetria! 🎉

Este documento fornece diretrizes para contribuir com o projeto.

## Código de Conduta

Ao participar deste projeto, você concorda em manter um ambiente respeitoso e colaborativo. Seja gentil e profissional em todas as interações.

## Como Posso Contribuir?

### Reportando Bugs

Antes de criar um relatório de bug, verifique se o problema já não foi reportado. Se você encontrar um bug:

1. **Use o template de issue** para bugs
2. **Seja específico** sobre o problema
3. **Inclua passos para reproduzir** o bug
4. **Forneça informações do ambiente**:
   - Versão do Python
   - Sistema operacional
   - Versões das bibliotecas relevantes

**Exemplo de bom relatório de bug:**

```
Título: Erro ao carregar arquivo CSV com caracteres especiais

Descrição:
O script jurimetria_completa.py falha ao processar arquivos CSV 
com caracteres especiais (ç, á, ã, etc.) nos nomes de juízes.

Passos para reproduzir:
1. Criar CSV com coluna 'juiz' contendo "José Araújo"
2. Executar: python3 jurimetria_completa.py
3. Observar erro de encoding

Ambiente:
- Python 3.10.5
- Ubuntu 22.04
- pandas 2.0.0

Erro esperado:
UnicodeDecodeError: 'utf-8' codec can't decode...
```

### Sugerindo Melhorias

Sugestões de melhorias são sempre bem-vindas! Para sugerir uma melhoria:

1. **Verifique se já não foi sugerida**
2. **Explique claramente o benefício**
3. **Forneça exemplos de uso**, se possível
4. **Considere alternativas**

### Pull Requests

Contribuições de código são muito apreciadas! Siga estes passos:

1. **Fork o projeto**
2. **Crie uma branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Faça commit das mudanças** (`git commit -m 'Add: MinhaFeature'`)
4. **Push para a branch** (`git push origin feature/MinhaFeature`)
5. **Abra um Pull Request**

#### Diretrizes para Pull Requests

- **Mantenha o código limpo e documentado**
- **Siga o estilo PEP 8** para código Python
- **Adicione testes** para novas funcionalidades
- **Atualize a documentação** conforme necessário
- **Certifique-se de que todos os testes passam**
- **Mantenha commits atômicos e com mensagens claras**

#### Padrão de Mensagens de Commit

Use mensagens descritivas seguindo este padrão:

```
Tipo: Descrição curta (máx 50 caracteres)

Descrição detalhada do que foi mudado e por quê.
Pode ter várias linhas.

Fixes #123
```

**Tipos de commit:**
- `Add:` Nova funcionalidade
- `Fix:` Correção de bug
- `Update:` Atualização de funcionalidade existente
- `Refactor:` Refatoração de código
- `Docs:` Mudanças na documentação
- `Test:` Adição ou correção de testes
- `Style:` Mudanças de formatação/estilo
- `Chore:` Tarefas de manutenção

**Exemplos:**
```
Add: Integração com API DataJud

Implementa cliente HTTP para coletar dados da API do DataJud.
Inclui rate limiting, retry logic e tratamento de erros.

Fixes #45
```

```
Fix: Erro de encoding ao ler CSV

Adiciona encoding='utf-8' explicitamente ao pandas.read_csv()
para evitar erros com caracteres especiais.

Fixes #67
```

## Processo de Desenvolvimento

### 1. Configuração do Ambiente

```bash
# Clone o repositório
git clone https://github.com/Joicerss/projeto-novo.git
cd projeto-novo

# Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instale dependências de desenvolvimento
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### 2. Executando Testes

```bash
# Executar todos os testes
pytest test_jurimetria.py -v

# Executar com cobertura
pytest test_jurimetria.py --cov=. --cov-report=html

# Executar testes específicos
pytest test_jurimetria.py::TestGeracaoDados -v
```

### 3. Verificação de Estilo

```bash
# Verificar estilo com flake8
flake8 *.py --max-line-length=120

# Formatar código com black
black *.py --line-length=120

# Verificar tipos com mypy
mypy jurimetria_completa.py --ignore-missing-imports
```

### 4. Documentação

Ao adicionar novas funcionalidades:

- **Docstrings**: Use docstrings em formato NumPy/Google
- **Comentários**: Adicione comentários explicativos quando necessário
- **README**: Atualize o README.md se aplicável
- **CHANGELOG**: Adicione entrada no CHANGELOG.md

**Exemplo de docstring:**

```python
def calcular_taxa_procedencia(df: pd.DataFrame, filtro: str = None) -> float:
    """
    Calcula a taxa de procedência de processos.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com coluna 'resultado'
    filtro : str, optional
        Filtro para aplicar (ex: 'classe == "Cível"')
        
    Returns
    -------
    float
        Taxa de procedência (entre 0 e 1)
        
    Examples
    --------
    >>> df = gerar_dados_simulados(100)
    >>> taxa = calcular_taxa_procedencia(df)
    >>> print(f"Taxa: {taxa:.2%}")
    Taxa: 57.33%
    """
    if filtro:
        df = df.query(filtro)
    return df['resultado'].mean()
```

## Áreas para Contribuir

Algumas áreas onde contribuições são especialmente bem-vindas:

### 🔴 Alta Prioridade
- Integração real com API DataJud
- Testes de integração
- Melhorias de performance
- Tratamento de dados ausentes/outliers

### 🟡 Média Prioridade
- Dashboard interativo
- Mais tipos de análises estatísticas
- Exportação para PDF
- API REST

### 🟢 Baixa Prioridade
- Suporte a outros idiomas
- Temas customizados para gráficos
- Integração com outras bases de dados judiciais
- Plugins/extensões

## Recursos Úteis

- [Documentação Python](https://docs.python.org/pt-br/3/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [PEP 8 - Style Guide](https://pep8.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

## Dúvidas?

Se você tiver dúvidas sobre como contribuir:

1. Verifique a [documentação](README.md)
2. Procure em [issues existentes](https://github.com/Joicerss/projeto-novo/issues)
3. Abra uma nova issue com a tag `question`

## Agradecimentos

Agradecemos a todos os contribuidores que ajudam a melhorar este projeto! 🙏

---

**Lembre-se:** Contribuições de qualquer tamanho são valiosas. Seja corrigindo um typo na documentação ou implementando uma feature complexa, sua ajuda é apreciada!
