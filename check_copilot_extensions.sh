#!/bin/bash
# Script to check GitHub Copilot extensions installation status
# Passo 1: Verificar se GitHub Copilot / GitHub Copilot Chat estão Installed

echo "============================================================"
echo "Passo 1: Verificando extensões do GitHub Copilot"
echo "============================================================"
echo ""

# Check if VS Code is installed
if ! command -v code &> /dev/null; then
    echo "⚠️  VS Code CLI não encontrado."
    echo "   Certifique-se de que o VS Code está instalado e"
    echo "   o comando 'code' está disponível no PATH."
    echo ""
    echo "Encontrei: VS Code não detectado"
    exit 1
fi

echo "✓ VS Code detectado"
echo ""

# Get list of installed extensions
echo "Verificando extensões..."
EXTENSIONS=$(code --list-extensions 2>/dev/null)

# Check for GitHub Copilot
COPILOT_INSTALLED="false"
COPILOT_CHAT_INSTALLED="false"

if echo "$EXTENSIONS" | grep -q "GitHub.copilot$"; then
    COPILOT_INSTALLED="true"
fi

if echo "$EXTENSIONS" | grep -q "GitHub.copilot-chat"; then
    COPILOT_CHAT_INSTALLED="true"
fi

echo ""
echo "------------------------------------------------------------"
echo "RESULTADO:"
echo "------------------------------------------------------------"

# Report results
if [ "$COPILOT_INSTALLED" = "true" ]; then
    echo "✓ GitHub Copilot: Installed"
else
    echo "✗ GitHub Copilot: Install"
fi

if [ "$COPILOT_CHAT_INSTALLED" = "true" ]; then
    echo "✓ GitHub Copilot Chat: Installed"
else
    echo "✗ GitHub Copilot Chat: Install"
fi

echo ""
echo "============================================================"

# Summary
if [ "$COPILOT_INSTALLED" = "true" ] && [ "$COPILOT_CHAT_INSTALLED" = "true" ]; then
    echo "Encontrei: Ambas as extensões estão Installed ✓"
    echo ""
    echo "Próximo passo: Sign in com GitHub Copilot"
    echo "============================================================"
    exit 0
else
    echo "Encontrei: Algumas extensões precisam ser Install"
    echo ""
    echo "Por favor, instale as extensões faltantes antes de prosseguir."
    echo "Você pode instalar executando:"
    
    if [ "$COPILOT_INSTALLED" = "false" ]; then
        echo "  code --install-extension GitHub.copilot"
    fi
    
    if [ "$COPILOT_CHAT_INSTALLED" = "false" ]; then
        echo "  code --install-extension GitHub.copilot-chat"
    fi
    
    echo "============================================================"
    exit 1
fi
