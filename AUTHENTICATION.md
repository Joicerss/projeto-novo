# Sistema de Autenticação / Authentication System

Este projeto agora inclui um sistema de autenticação baseado em token para proteger o acesso à geração de relatórios.

This project now includes a token-based authentication system to protect access to report generation.

## Configuração Inicial / Initial Setup

### 1. Gerar um Token / Generate a Token

Primeiro, você precisa gerar um token de autenticação:

```bash
python token_manager.py gerar
```

ou / or

```bash
python token_manager.py generate
```

Este comando irá:
- Gerar um token seguro aleatório de 64 caracteres
- Salvar o hash do token em `projeto/token`
- Mostrar o token na tela (guarde-o em local seguro!)

This command will:
- Generate a secure random 64-character token
- Save the token hash in `projeto/token`
- Display the token on screen (save it in a secure location!)

⚠️ **IMPORTANTE / IMPORTANT**: O token será mostrado apenas uma vez. Guarde-o com segurança!

⚠️ **IMPORTANT**: The token will only be shown once. Keep it safe!

### 2. Usar o Sistema / Using the System

#### Gerar Relatório / Generate Report

Para gerar o relatório, você agora precisa fornecer o token:

```bash
python generate_report_complete.py SEU_TOKEN_AQUI
```

ou / or

```bash
python generate_report_complete.py YOUR_TOKEN_HERE
```

#### Verificar um Token / Verify a Token

Para verificar se um token é válido:

```bash
python token_manager.py verificar SEU_TOKEN
```

ou / or

```bash
python token_manager.py verify YOUR_TOKEN
```

## Segurança / Security

- O token original **nunca** é armazenado. Apenas o hash SHA-256 é salvo.
- Tokens são comparados usando `secrets.compare_digest()` para prevenir ataques de timing.
- Tokens têm 64 caracteres hexadecimais (256 bits de entropia).

- The original token is **never** stored. Only the SHA-256 hash is saved.
- Tokens are compared using `secrets.compare_digest()` to prevent timing attacks.
- Tokens have 64 hexadecimal characters (256 bits of entropy).

## Estrutura de Arquivos / File Structure

```
projeto-novo/
├── auth.py                      # Módulo de autenticação / Authentication module
├── token_manager.py             # Gerenciador de tokens / Token manager
├── generate_report_complete.py  # Gerador de relatórios (protegido) / Report generator (protected)
├── projeto/
│   └── token                    # Hash do token armazenado / Stored token hash
└── AUTHENTICATION.md            # Esta documentação / This documentation
```

## Exemplos / Examples

### Exemplo Completo de Uso / Complete Usage Example

```bash
# 1. Gerar token pela primeira vez / Generate token for the first time
$ python token_manager.py gerar

============================================================
NOVO TOKEN GERADO:
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
============================================================

⚠️  IMPORTANTE: Guarde este token em local seguro!

# 2. Verificar o token (opcional) / Verify token (optional)
$ python token_manager.py verificar a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
✅ Token válido!

# 3. Gerar relatório com autenticação / Generate report with authentication
$ python generate_report_complete.py a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
✅ Autenticação bem-sucedida. Gerando relatório...
✅ Relatório completo gerado em: /path/to/report_complete.html
```

## Substituindo o Token / Replacing the Token

Se você precisar gerar um novo token:

If you need to generate a new token:

```bash
python token_manager.py gerar
```

O sistema irá perguntar se você deseja substituir o token existente.

The system will ask if you want to replace the existing token.

## Solução de Problemas / Troubleshooting

### Erro: "Sistema de autenticação não configurado"

Execute: `python token_manager.py gerar` para criar um token.

Run: `python token_manager.py generate` to create a token.

### Erro: "Token inválido"

Verifique se você está usando o token correto. O token é case-sensitive.

Check if you are using the correct token. The token is case-sensitive.

### Perdi meu token / I lost my token

Você precisará gerar um novo token: `python token_manager.py gerar`

You will need to generate a new token: `python token_manager.py generate`
