#!/bin/bash
# Script para verificar se as extensões do GitHub Copilot estão instaladas no VS Code
# Usage: ./check_copilot_extensions.sh

echo "=========================================="
echo "Verificação das Extensões GitHub Copilot"
echo "=========================================="
echo ""

# Verificar se o VS Code está instalado
if ! command -v code &> /dev/null; then
    echo "❌ VS Code não encontrado no PATH"
    echo "   Por favor, instale o VS Code ou adicione-o ao PATH"
    exit 1
fi

echo "✅ VS Code encontrado"
echo ""

# Listar extensões instaladas
echo "Verificando extensões instaladas..."
echo ""

COPILOT_INSTALLED=false
COPILOT_CHAT_INSTALLED=false

# Verificar GitHub Copilot
if code --list-extensions | grep -q "^github.copilot$"; then
    echo "✅ Encontrei: GitHub Copilot - INSTALLED"
    COPILOT_INSTALLED=true
else
    echo "❌ Encontrei: GitHub Copilot - NOT INSTALLED"
fi

# Verificar GitHub Copilot Chat
if code --list-extensions | grep -q "^github.copilot-chat$"; then
    echo "✅ Encontrei: GitHub Copilot Chat - INSTALLED"
    COPILOT_CHAT_INSTALLED=true
else
    echo "❌ Encontrei: GitHub Copilot Chat - NOT INSTALLED"
fi

echo ""
echo "=========================================="

# Instruções baseadas no resultado
if [ "$COPILOT_INSTALLED" = true ] && [ "$COPILOT_CHAT_INSTALLED" = true ]; then
    echo "🎉 Todas as extensões necessárias estão instaladas!"
    echo ""
    echo "Próximo passo: Sign In"
    echo "  1. Abra o VS Code"
    echo "  2. Pressione Ctrl+Shift+P (ou Cmd+Shift+P no Mac)"
    echo "  3. Digite: 'GitHub Copilot: Sign In'"
    echo "  4. Siga as instruções no navegador"
elif [ "$COPILOT_INSTALLED" = true ] || [ "$COPILOT_CHAT_INSTALLED" = true ]; then
    echo "⚠️  Algumas extensões estão faltando"
    echo ""
    echo "Para instalar as extensões faltantes:"
    [ "$COPILOT_INSTALLED" = false ] && echo "  code --install-extension github.copilot"
    [ "$COPILOT_CHAT_INSTALLED" = false ] && echo "  code --install-extension github.copilot-chat"
else
    echo "❌ Nenhuma extensão do Copilot encontrada"
    echo ""
    echo "Para instalar todas as extensões:"
    echo "  code --install-extension github.copilot"
    echo "  code --install-extension github.copilot-chat"
fi

echo ""
echo "Para mais informações, veja: VERIFICACAO_COPILOT.md"
echo "=========================================="
