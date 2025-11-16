# Verificador de Extensões GitHub Copilot

Script para verificar se as extensões GitHub Copilot e GitHub Copilot Chat estão instaladas no VS Code.

## Uso

Execute o script com Python 3:

```bash
python3 check_copilot_extensions.py
```

## O que o script faz

### Passo 1: Verifica extensões instaladas

O script realiza as seguintes ações:

1. **Verificação automática (se VS Code CLI disponível)**:
   - Executa `code --list-extensions` para listar extensões instaladas
   - Verifica se `GitHub.copilot` e `GitHub.copilot-chat` estão na lista
   - Reporta o status: "Installed" ou "Install"

2. **Verificação manual (se CLI não disponível)**:
   - Lê o arquivo `.vscode/extensions.json` para ver extensões recomendadas
   - Fornece instruções para verificação manual no VS Code
   - Solicita que o usuário reporte o status

### Saída esperada

Quando as extensões estão instaladas:
```
encontrei:
  ✓ GitHub Copilot: Installed
  ✓ GitHub Copilot Chat: Installed

Próximo passo: Sign in (aguardando comando...)
```

Quando as extensões precisam ser instaladas:
```
encontrei:
  ⚠ GitHub Copilot: Install
  ⚠ GitHub Copilot Chat: Install

Próximo passo: Sign in (aguardando comando...)
```

## Códigos de saída

- `0`: Todas as extensões estão instaladas
- `1`: Algumas extensões precisam ser instaladas
- `2`: Verificação manual necessária (CLI não disponível)

## Verificação manual no VS Code

Se o script solicitar verificação manual:

1. Abra o VS Code
2. Pressione `Ctrl+Shift+X` (Windows/Linux) ou `Cmd+Shift+X` (Mac)
3. Procure por "GitHub Copilot" e "GitHub Copilot Chat"
4. Verifique se o botão mostra:
   - "Installed" (verde com check) = extensão instalada
   - "Install" (azul) = precisa instalar

## Extensões recomendadas

O projeto recomenda as seguintes extensões no arquivo `.vscode/extensions.json`:
- `GitHub.copilot` - GitHub Copilot
- `GitHub.copilot-chat` - GitHub Copilot Chat

Quando você abrir o projeto no VS Code, ele sugerirá instalar essas extensões automaticamente.

## Próximos passos

Após verificar que as extensões estão instaladas, o próximo passo é fazer Sign in no GitHub Copilot.
