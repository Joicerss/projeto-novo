# Guia Rápido — Instalação do GitHub Copilot no VS Code

## TL;DR — Instalação Rápida em 3 Passos

Se você encontrou o erro `ENOTFOUND next-waitlist.azurewebsites.net` ao tentar usar o Copilot CLI, siga estes passos para usar a **extensão VS Code** (funciona 100%):

### ✅ Passo 1: Instalar Extensão

**No VS Code:**
1. Clique no ícone Extensions (lado esquerdo) ou pressione `Ctrl+Shift+X`
2. Busque: `GitHub Copilot`
3. Instale as duas extensões oficiais:
   - **GitHub Copilot** (sugestões de código)
   - **GitHub Copilot Chat** (chat interativo)

**Via comando (alternativa):**
```powershell
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
```

### ✅ Passo 2: Fazer Login

1. Pressione `Ctrl+Shift+P` no VS Code
2. Digite: `GitHub: Sign in`
3. Siga o fluxo no navegador (login GitHub + autorizar)
4. Volte ao VS Code → pronto! ✓

### ✅ Passo 3: Testar

**Teste rápido:**
1. Abra qualquer arquivo `.py`, `.js`, `.java`, etc.
2. Comece a digitar código
3. Sugestões em cinza aparecerão → pressione `Tab` para aceitar

**Ou abra o chat:**
- Pressione `Ctrl+Shift+P` → digite `Copilot: Chat`

---

## Por que o CLI não funciona?

O erro acontece porque o endpoint `next-waitlist.azurewebsites.net` usado pelo CLI não está resolvendo (DNS retorna NXDOMAIN). Possíveis causas:

- ❌ Serviço temporariamente fora do ar
- ❌ Firewall ou rede corporativa bloqueando
- ❌ Endpoint migrado/descontinuado

**A extensão VS Code funciona** porque usa um fluxo OAuth diferente que não depende desse endpoint.

---

## Precisa do CLI mesmo assim?

Se você **realmente** precisa do CLI (não da extensão), tente:

### Opção A: Via Hotspot Móvel

```powershell
# 1. Ative hotspot do celular e conecte o PC
# 2. Execute:
& "C:\Program Files\nodejs\npx.cmd" --yes @githubnext/github-copilot-cli auth login
```

### Opção B: Via VPN

Conecte-se a uma VPN e tente o comando acima novamente.

---

## Troubleshooting

### ❓ Extensão instalada mas não aparece?

1. Recarregue o VS Code: `Ctrl+Shift+P` → `Reload Window`
2. Verifique se está logado: canto inferior esquerdo deve mostrar seu usuário GitHub

### ❓ Sugestões não aparecem?

1. Abra Configurações: `Ctrl+,`
2. Busque: `Copilot: Enable`
3. Certifique-se que está marcado ✓

### ❓ Erro "You don't have access to Copilot"?

Verifique sua licença em: https://github.com/settings/copilot

---

## Links Úteis

- 📚 [Guia completo de troubleshooting](COPILOT_TROUBLESHOOTING.md) (este repo)
- 📖 [Documentação oficial do Copilot](https://docs.github.com/copilot)
- 🔧 [Status do GitHub](https://www.githubstatus.com/)

---

**Problema resolvido?** Volte ao seu código! 🚀

**Ainda com problemas?** Consulte o [guia completo](COPILOT_TROUBLESHOOTING.md) ou abra um issue.
