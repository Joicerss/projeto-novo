#!/usr/bin/env python3
"""
Script to check if GitHub Copilot and GitHub Copilot Chat extensions are installed in VS Code.
Reports status in Portuguese: "encontrei" + installation status.
"""

import subprocess
import sys
import json
import os
from pathlib import Path

def check_vscode_extensions_via_cli():
    """
    Check if GitHub Copilot extensions are installed in VS Code using CLI.
    Returns a dictionary with extension names and their installation status, or None if CLI not available.
    """
    extensions_to_check = {
        "GitHub.copilot": "GitHub Copilot",
        "GitHub.copilot-chat": "GitHub Copilot Chat"
    }
    
    results = {}
    
    try:
        # Run 'code --list-extensions' to get installed extensions
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        
        installed_extensions = result.stdout.strip().split('\n')
        installed_extensions = [ext.strip() for ext in installed_extensions if ext.strip()]
        
        # Check each extension
        for ext_id, ext_name in extensions_to_check.items():
            if ext_id in installed_extensions:
                results[ext_name] = "Installed"
            else:
                results[ext_name] = "Install"
        
        return results
                
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None

def check_extensions_json():
    """
    Check the .vscode/extensions.json file to see recommended extensions.
    Returns info about what's recommended.
    """
    extensions_json_path = Path(".vscode/extensions.json")
    
    if not extensions_json_path.exists():
        return None
    
    try:
        with open(extensions_json_path, 'r') as f:
            data = json.load(f)
            recommendations = data.get("recommendations", [])
            return recommendations
    except (json.JSONDecodeError, IOError):
        return None

def print_manual_instructions():
    """Print manual instructions for checking extensions."""
    print("\n" + "="*60)
    print("INSTRUÇÕES MANUAIS - Como verificar extensões no VS Code:")
    print("="*60)
    print("\n1. Abra o VS Code")
    print("2. Pressione Ctrl+Shift+X (Windows/Linux) ou Cmd+Shift+X (Mac)")
    print("   para abrir a visualização de Extensions")
    print("\n3. Procure por:")
    print("   - 'GitHub Copilot'")
    print("   - 'GitHub Copilot Chat'")
    print("\n4. Verifique se elas aparecem como:")
    print("   - 'Installed' (instalado) - botão verde com check")
    print("   - 'Install' (precisa instalar) - botão azul Install")
    print("\n5. Reporte o status encontrado.")
    print("="*60 + "\n")

def main():
    """Main function to check extensions and report status."""
    print("="*60)
    print("Passo 1: Verificando extensões do GitHub Copilot")
    print("="*60 + "\n")
    
    # Try CLI method first
    results = check_vscode_extensions_via_cli()
    
    if results is not None:
        # CLI method worked
        print("✓ Verificação automática via VS Code CLI\n")
        print("encontrei:")
        for ext_name, status in results.items():
            status_icon = "✓" if status == "Installed" else "⚠"
            print(f"  {status_icon} {ext_name}: {status}")
        
        all_installed = all(status == "Installed" for status in results.values())
        
        if all_installed:
            print("\n✓ Todas as extensões estão instaladas!")
        else:
            print("\n⚠ Algumas extensões precisam ser instaladas.")
        
        print("\n" + "="*60)
        print("Próximo passo: Sign in (aguardando comando...)")
        print("="*60)
        
        return 0 if all_installed else 1
    else:
        # CLI not available, check extensions.json and provide manual instructions
        print("⚠ VS Code CLI não disponível neste ambiente.\n")
        
        # Check what's recommended in extensions.json
        recommendations = check_extensions_json()
        if recommendations:
            print("Extensões recomendadas em .vscode/extensions.json:")
            for rec in recommendations:
                print(f"  - {rec}")
            print()
        
        # Provide manual instructions
        print_manual_instructions()
        
        print("Por favor, execute as instruções manuais acima e reporte:")
        print("encontrei: [status das extensões]")
        print("\nExemplo de resposta esperada:")
        print("  encontrei:")
        print("  - GitHub Copilot: Installed")
        print("  - GitHub Copilot Chat: Installed")
        print("\nOU")
        print("  encontrei:")
        print("  - GitHub Copilot: Install")
        print("  - GitHub Copilot Chat: Install")
        
        return 2  # Exit code 2 indicates manual check needed

if __name__ == "__main__":
    sys.exit(main())
