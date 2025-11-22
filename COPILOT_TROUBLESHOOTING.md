# Guia de Solução de Problemas — GitHub Copilot

Este documento fornece orientações para resolver problemas de instalação e autenticação do GitHub Copilot.

## Índice

- [Contexto do Problema](#contexto-do-problema)
- [Opções de Solução](#opções-de-solução)
  - [Opção 1: Instalar Extensão Copilot no VS Code (Recomendado) ✅](#opção-1-instalar-extensão-copilot-no-vs-code-recomendado-)
  - [Opção 2: Autenticar CLI via Hotspot/VPN](#opção-2-autenticar-cli-via-hotspotVPN)
  - [Opção 3: Gerar Log de Diagnóstico](#opção-3-gerar-log-de-diagnóstico)
  - [Opção 4: Explicação Detalhada](#opção-4-explicação-detalhada)
- [Comparação das Opções](#comparação-das-opções)
- [Perguntas Frequentes](#perguntas-frequentes)
- [Suporte Adicional](#suporte-adicional)
- [Resumo — Decisão Rápida](#resumo--decisão-rápida)

## Contexto do Problema

Durante a tentativa de autenticar o Copilot CLI, pode ocorrer o seguinte erro:

```
getaddrinfo ENOTFOUND next-waitlist.azurewebsites.net
```

Isso acontece quando o host `next-waitlist.azurewebsites.net` não resolve publicamente (NXDOMAIN), impedindo que o CLI troque o código de dispositivo pelo token de autenticação.

### Ambiente Verificado

- Node.js: v24.11.1
- npm/npx: 11.6.2
- DNS testado: Local, 8.8.8.8 (Google), 1.1.1.1 (Cloudflare) — todos retornaram NXDOMAIN

## Opções de Solução

Escolha uma das opções abaixo conforme sua necessidade:

### Opção 1: Instalar Extensão Copilot no VS Code (Recomendado) ✅

Esta é a solução mais rápida e eficaz para começar a usar o Copilot imediatamente.

#### Passo 1: Abrir o VS Code

Abra o Visual Studio Code no seu computador.

#### Passo 2: Instalar a Extensão

**Método A - Interface Gráfica (Recomendado):**

1. Clique no ícone de **Extensions** (quadrado com 4 blocos) na barra lateral esquerda
2. Na barra de pesquisa, digite: `GitHub Copilot` ou `Copilot Chat`
3. Localize a extensão oficial publicada por **GitHub**
4. Clique no botão **Install**

**Método B - Linha de Comando:**

Se o comando `code` estiver disponível no seu PowerShell:

```powershell
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
```

#### Passo 3: Autenticação

1. Após a instalação, aparecerá uma notificação **"Sign in to GitHub"** — aceite-a
   
   **OU**
   
2. Abra a Paleta de Comandos:
   - Pressione `Ctrl+Shift+P` (Windows/Linux) ou `Cmd+Shift+P` (Mac)
   - Digite: `GitHub: Sign in` ou `Copilot: Sign in`
   - Pressione Enter

3. O VS Code abrirá seu navegador padrão
4. Entre na sua conta GitHub
5. Autorize o acesso quando solicitado
6. Retorne ao VS Code — deve aparecer "Signed in" ✓

#### Passo 4: Teste

**Teste 1 - Chat do Copilot:**
1. Pressione `Ctrl+Shift+P`
2. Digite: `Copilot: Chat`
3. O painel de chat deve abrir

**Teste 2 - Sugestões Inline:**
1. Abra qualquer arquivo de código (`.py`, `.js`, `.java`, etc.)
2. Comece a digitar código
3. O Copilot oferecerá sugestões em cinza claro
4. Pressione `Tab` para aceitar uma sugestão

### Opção 2: Autenticar CLI via Hotspot/VPN

Use esta opção se precisar especificamente do Copilot CLI e suspeita de problemas de rede.

#### Passos:

1. **Ative o hotspot do celular** e conecte seu PC a ele
   
   OU
   
2. **Conecte-se a uma VPN** confiável

3. Abra um novo terminal PowerShell

4. Execute o comando de autenticação:

```powershell
& "C:\Program Files\nodejs\npx.cmd" --yes @githubnext/github-copilot-cli auth login
```

5. Siga as instruções na tela:
   - Um código de dispositivo será exibido
   - Abra o URL fornecido no navegador
   - Insira o código
   - Autorize o acesso

6. Se bem-sucedido, você verá a mensagem de confirmação de autenticação

### Opção 3: Gerar Log de Diagnóstico

Use esta opção se as anteriores não funcionarem e você precisar investigar o problema mais a fundo.

#### Passos:

1. Abra o PowerShell

2. Execute o seguinte comando para capturar o log completo:

```powershell
& "C:\Program Files\nodejs\npx.cmd" --yes @githubnext/github-copilot-cli auth login 2>&1 | Out-File copilot-auth-log.txt -Encoding utf8; notepad copilot-auth-log.txt
```

3. O Notepad abrirá com o arquivo de log

4. Copie as últimas ~40 linhas do log

5. Compartilhe o log com o suporte técnico ou em um issue no repositório

#### O que procurar no log:

- Erros de DNS (`ENOTFOUND`, `NXDOMAIN`)
- Timeouts de conexão
- Erros de certificado SSL/TLS
- Mensagens de firewall ou proxy

### Opção 4: Explicação Detalhada

Se você precisa de mais contexto antes de escolher uma opção:

#### Por que o CLI está falando?

O Copilot CLI depende do endpoint `next-waitlist.azurewebsites.net` para completar o fluxo de autenticação OAuth device code. Quando este host não resolve:

- Seu DNS local não consegue encontrar o IP
- DNS públicos (8.8.8.8, 1.1.1.1) também falham
- Possíveis causas:
  - O serviço pode estar temporariamente fora do ar
  - Pode haver bloqueio de firewall/rede corporativa
  - O endpoint pode ter sido migrado ou descontinuado

#### Por que a extensão VS Code funciona?

A extensão do VS Code usa um fluxo de autenticação diferente:

- Usa o navegador diretamente para OAuth
- Não depende do endpoint `next-waitlist.azurewebsites.net`
- Autenticação gerenciada pela própria plataforma GitHub
- Mais resiliente a problemas de rede específicos

## Comparação das Opções

| Critério | VS Code Extension | CLI via Hotspot | Log Diagnóstico |
|----------|-------------------|-----------------|-----------------|
| Velocidade | ⚡ Rápido (5-10 min) | 🕐 Médio (10-15 min) | 🕐 Variável |
| Complexidade | ✅ Simples | ⚠️ Requer acesso móvel | 🔧 Técnico |
| Taxa de Sucesso | 🟢 Alta (~95%) | 🟡 Média (~70%) | 📊 Diagnóstico |
| Recomendado Para | Uso geral no VS Code | Usuários de CLI | Troubleshooting |

## Perguntas Frequentes

### Posso usar ambos (extensão e CLI)?

Sim! A extensão VS Code e o CLI são independentes. Você pode:
- Usar a extensão para desenvolvimento no VS Code
- Usar o CLI para comandos no terminal
- Ambos compartilham a mesma conta GitHub

### O que fazer se a extensão também falhar?

1. Verifique se sua conta GitHub tem acesso ao Copilot:
   - Acesse: https://github.com/settings/copilot
   - Confirme que você tem uma licença ativa

2. Verifique conexão com GitHub:
   ```powershell
   Test-NetConnection github.com -Port 443
   ```

3. Tente desabilitar temporariamente firewall/antivírus

### Como atualizar a extensão?

No VS Code:
1. Vá para Extensions
2. Procure por "GitHub Copilot"
3. Se houver atualização, clique em "Update"

### Como desinstalar se necessário?

**Extensão VS Code:**
1. Extensions → GitHub Copilot → Uninstall

**CLI:**
```powershell
npm uninstall -g @githubnext/github-copilot-cli
```

## Suporte Adicional

Se nenhuma opção resolver seu problema:

1. **Documentação Oficial:**
   - https://docs.github.com/copilot

2. **Status do Serviço:**
   - https://www.githubstatus.com/

3. **Comunidade:**
   - https://github.community/

4. **Suporte GitHub:**
   - https://support.github.com/

## Resumo — Decisão Rápida

```
┌─────────────────────────────────────┐
│  Você usa principalmente VS Code?   │
└─────────────────┬───────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
        SIM               NÃO
         │                 │
         ▼                 ▼
   OPÇÃO 1          OPÇÃO 2 ou 3
   (VS Code)        (CLI/Diagnóstico)
```

**Resposta Rápida:** Digite na resposta:
- `"Instalar agora"` → seguir Opção 1
- `"Hotspot"` → seguir Opção 2
- `"Gerar log"` → seguir Opção 3
- `"Parar/explicar"` → reler Opção 4

---

**Última atualização:** 2025-11-16
