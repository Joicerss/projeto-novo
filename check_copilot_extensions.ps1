# PowerShell script to check GitHub Copilot extensions installation status
# Passo 1: Verificar se GitHub Copilot / GitHub Copilot Chat estão Installed

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Passo 1: Verificando extensões do GitHub Copilot" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if VS Code is installed
$codeCommand = Get-Command code -ErrorAction SilentlyContinue

if (-not $codeCommand) {
    Write-Host "⚠️  VS Code CLI não encontrado." -ForegroundColor Yellow
    Write-Host "   Certifique-se de que o VS Code está instalado e"
    Write-Host "   o comando 'code' está disponível no PATH."
    Write-Host ""
    Write-Host "Encontrei: VS Code não detectado" -ForegroundColor Red
    exit 1
}

Write-Host "✓ VS Code detectado" -ForegroundColor Green
Write-Host ""

# Get list of installed extensions
Write-Host "Verificando extensões..."
try {
    $extensions = & code --list-extensions 2>$null
} catch {
    Write-Host "Erro ao obter lista de extensões" -ForegroundColor Red
    exit 1
}

# Check for GitHub Copilot extensions
$copilotInstalled = $extensions -contains "GitHub.copilot"
$copilotChatInstalled = $extensions -contains "GitHub.copilot-chat"

Write-Host ""
Write-Host "------------------------------------------------------------" -ForegroundColor Cyan
Write-Host "RESULTADO:" -ForegroundColor Cyan
Write-Host "------------------------------------------------------------" -ForegroundColor Cyan

# Report results
if ($copilotInstalled) {
    Write-Host "✓ GitHub Copilot: Installed" -ForegroundColor Green
} else {
    Write-Host "✗ GitHub Copilot: Install" -ForegroundColor Red
}

if ($copilotChatInstalled) {
    Write-Host "✓ GitHub Copilot Chat: Installed" -ForegroundColor Green
} else {
    Write-Host "✗ GitHub Copilot Chat: Install" -ForegroundColor Red
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

# Summary
if ($copilotInstalled -and $copilotChatInstalled) {
    Write-Host "Encontrei: Ambas as extensões estão Installed ✓" -ForegroundColor Green
    Write-Host ""
    Write-Host "Próximo passo: Sign in com GitHub Copilot" -ForegroundColor Yellow
    Write-Host "============================================================" -ForegroundColor Cyan
    exit 0
} else {
    Write-Host "Encontrei: Algumas extensões precisam ser Install" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Por favor, instale as extensões faltantes antes de prosseguir."
    Write-Host "Você pode instalar executando:"
    
    if (-not $copilotInstalled) {
        Write-Host "  code --install-extension GitHub.copilot" -ForegroundColor White
    }
    
    if (-not $copilotChatInstalled) {
        Write-Host "  code --install-extension GitHub.copilot-chat" -ForegroundColor White
    }
    
    Write-Host "============================================================" -ForegroundColor Cyan
    exit 1
}
