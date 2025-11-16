#!/usr/bin/env python3
"""
Script to check if GitHub Copilot extensions are installed in VS Code.
This implements "Passo 1" - checking extension installation status.
"""

import subprocess
import sys
import json
import os
from pathlib import Path


def check_vscode_installed():
    """Check if VS Code CLI is available."""
    try:
        result = subprocess.run(
            ["code", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_installed_extensions():
    """Get list of installed VS Code extensions."""
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')
        return []
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print(f"Erro ao obter extensões: {e}", file=sys.stderr)
        return []


def check_copilot_extensions():
    """
    Check if GitHub Copilot extensions are installed.
    Returns a dict with extension status.
    """
    # Extension IDs for GitHub Copilot
    copilot_extension = "GitHub.copilot"
    copilot_chat_extension = "GitHub.copilot-chat"
    
    extensions_to_check = {
        "GitHub Copilot": copilot_extension,
        "GitHub Copilot Chat": copilot_chat_extension
    }
    
    # Get installed extensions
    installed = get_installed_extensions()
    
    # Check each extension
    results = {}
    for name, ext_id in extensions_to_check.items():
        if ext_id in installed:
            results[name] = "Installed"
        else:
            results[name] = "Install"
    
    return results


def main():
    """Main function to check and report Copilot extension status."""
    print("=" * 60)
    print("Passo 1: Verificando extensões do GitHub Copilot")
    print("=" * 60)
    print()
    
    # Check if VS Code is installed
    if not check_vscode_installed():
        print("⚠️  VS Code CLI não encontrado.")
        print("   Certifique-se de que o VS Code está instalado e")
        print("   o comando 'code' está disponível no PATH.")
        print()
        print("Encontrei: VS Code não detectado")
        return 1
    
    print("✓ VS Code detectado")
    print()
    
    # Check extensions
    print("Verificando extensões...")
    results = check_copilot_extensions()
    
    print()
    print("-" * 60)
    print("RESULTADO:")
    print("-" * 60)
    
    # Report findings
    all_installed = True
    for ext_name, status in results.items():
        status_icon = "✓" if status == "Installed" else "✗"
        print(f"{status_icon} {ext_name}: {status}")
        if status != "Installed":
            all_installed = False
    
    print()
    print("=" * 60)
    
    # Summary message
    if all_installed:
        print("Encontrei: Ambas as extensões estão Installed ✓")
        print()
        print("Próximo passo: Sign in com GitHub Copilot")
    else:
        print("Encontrei: Algumas extensões precisam ser Install")
        print()
        print("Por favor, instale as extensões faltantes antes de prosseguir.")
        print("Você pode instalar executando:")
        for ext_name, status in results.items():
            if status == "Install":
                ext_id = "GitHub.copilot" if "Chat" not in ext_name else "GitHub.copilot-chat"
                print(f"  code --install-extension {ext_id}")
    
    print("=" * 60)
    
    return 0 if all_installed else 1


if __name__ == "__main__":
    sys.exit(main())
