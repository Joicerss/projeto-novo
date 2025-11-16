# Verificação de Instalação do GitHub Copilot

## Passo 1: Verificar se as Extensões estão Instaladas

### Opção A: Usando o Script Automatizado (Linux/Mac/Git Bash)

Execute o script fornecido:

```bash
./check_copilot_extensions.sh
```

Este script verificará automaticamente se as extensões estão instaladas e informará o status.

### Opção B: Verificação Manual no Visual Studio Code:

1. **Abra a aba de Extensões:**
   - Pressione `Ctrl+Shift+X` (Windows/Linux) ou `Cmd+Shift+X` (Mac)
   - Ou clique no ícone de Extensões na barra lateral esquerda

2. **Procure pelas seguintes extensões:**
   - **GitHub Copilot** (ID: `github.copilot`)
   - **GitHub Copilot Chat** (ID: `github.copilot-chat`)

3. **Verifique o status:**
   - Se aparecer **"Installed"** (Instalado) ✅ - As extensões já estão instaladas
   - Se aparecer **"Install"** (Instalar) ❌ - Você precisa instalar as extensões

### Resultado Esperado:

**Encontrei:** 
- GitHub Copilot: [Installed / Install]
- GitHub Copilot Chat: [Installed / Install]

---

## Passo 2: Instalar as Extensões (se necessário)

Se as extensões não estiverem instaladas:

1. Clique no botão **"Install"** para cada extensão
2. Aguarde a instalação ser concluída
3. Pode ser necessário recarregar o VS Code

---

## Passo 3: Sign In (Entrar)

Após instalar as extensões:

1. **Abra a Command Palette:**
   - Pressione `Ctrl+Shift+P` (Windows/Linux) ou `Cmd+Shift+P` (Mac)

2. **Execute o comando de Sign In:**
   - Digite: `GitHub Copilot: Sign In`
   - Pressione Enter

3. **Autentique-se:**
   - Uma janela do navegador será aberta
   - Faça login com sua conta GitHub
   - Autorize o GitHub Copilot
   - Aguarde a confirmação

4. **Verifique o status:**
   - No canto inferior direito do VS Code, você verá o ícone do Copilot
   - Se estiver ativo, o ícone estará colorido ✅
   - Se houver problemas, o ícone estará acinzentado ou com um aviso ⚠️

---

## Logs e Troubleshooting

### Verificar Logs do Copilot:

1. Abra a Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Digite: `Developer: Show Logs`
3. Selecione `GitHub Copilot`

### Problemas Comuns:

- **Extensão instalada mas não funciona:** Verifique se você tem uma licença ativa do GitHub Copilot
- **Erro de autenticação:** Tente deslogar e logar novamente
- **Sugestões não aparecem:** Verifique se o Copilot está habilitado para o tipo de arquivo atual

---

## Extensões Recomendadas

Este projeto já está configurado com um arquivo `.vscode/extensions.json` que recomenda automaticamente:
- GitHub Copilot
- GitHub Copilot Chat

Ao abrir o projeto no VS Code, você receberá uma notificação para instalar as extensões recomendadas.

---

## Comandos Úteis do Copilot

- **Abrir Chat:** `Ctrl+I` ou clique no ícone do chat
- **Sugestões inline:** Digite código e aguarde as sugestões aparecerem
- **Próxima sugestão:** `Alt+]` (Windows/Linux) ou `Option+]` (Mac)
- **Sugestão anterior:** `Alt+[` (Windows/Linux) ou `Option+[` (Mac)
- **Aceitar sugestão:** `Tab`
- **Rejeitar sugestão:** `Esc`
