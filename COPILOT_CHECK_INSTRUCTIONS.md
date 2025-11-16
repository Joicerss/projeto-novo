# GitHub Copilot Extension Check - Passo 1

Este documento fornece instruções para verificar se as extensões do GitHub Copilot estão instaladas.

## Método Automático (Recomendado)

Execute o script Python fornecido:

```bash
python3 check_copilot_extensions.py
```

O script irá:
1. Verificar se o VS Code está instalado
2. Listar as extensões instaladas
3. Verificar se GitHub Copilot e GitHub Copilot Chat estão instalados
4. Reportar o status com "Encontrei: [status]"

## Método Manual

Se preferir verificar manualmente:

### Via VS Code UI

1. Abra o VS Code
2. Pressione `Ctrl+Shift+X` (Windows/Linux) ou `Cmd+Shift+X` (Mac) para abrir a aba Extensions
3. Procure por "GitHub Copilot" na barra de pesquisa
4. Verifique se as seguintes extensões aparecem como "Installed":
   - **GitHub Copilot** (ID: `GitHub.copilot`)
   - **GitHub Copilot Chat** (ID: `GitHub.copilot-chat`)

### Via Command Line

Execute o seguinte comando no terminal:

```bash
code --list-extensions | grep -i copilot
```

Você deve ver:
```
GitHub.copilot
GitHub.copilot-chat
```

## Resultados Esperados

### Se ambas estão instaladas:
```
Encontrei: Ambas as extensões estão Installed ✓
```

### Se alguma não está instalada:
```
Encontrei: Algumas extensões precisam ser Install
```

## Próximos Passos

Após verificar que as extensões estão instaladas:
1. **Próximo comando**: Sign in com GitHub Copilot
2. Aguarde o resultado do navegador/logs para autenticação

## Instalação (se necessário)

Se alguma extensão não estiver instalada:

```bash
# Instalar GitHub Copilot
code --install-extension GitHub.copilot

# Instalar GitHub Copilot Chat
code --install-extension GitHub.copilot-chat
```

Ou instale via VS Code UI:
1. Abra Extensions (`Ctrl+Shift+X` / `Cmd+Shift+X`)
2. Pesquise "GitHub Copilot"
3. Clique em "Install" nas extensões necessárias
