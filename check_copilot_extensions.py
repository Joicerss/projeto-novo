#!/usr/bin/env python3
"""
Script para verificar se as extensões GitHub Copilot e GitHub Copilot Chat estão instaladas no VS Code.
Reporta o status em português: "encontrei" + status de instalação.
"""

import subprocess
import sys
import json
import os
from pathlib import Path

def check_vscode_extensions_via_cli():
    """
    Verifica se as extensões GitHub Copilot estão instaladas no VS Code usando CLI.
    Retorna um dicionário com os nomes das extensões e seus status de instalação, ou None se CLI não disponível.
    """
    extensions_to_check = {
        "GitHub.copilot": "GitHub Copilot",
        "GitHub.copilot-chat": "GitHub Copilot Chat"
    }
    
    results = {}
    
    try:
        # Executa 'code --list-extensions' para obter extensões instaladas
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        
        installed_extensions = result.stdout.strip().split('\n')
        installed_extensions = [ext.strip() for ext in installed_extensions if ext.strip()]
        
        # Verifica cada extensão
        for ext_id, ext_name in extensions_to_check.items():
            if ext_id in installed_extensions:
                results[ext_name] = "Instalado"
            else:
                results[ext_name] = "Instalar"
        
        return results
                
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None

def check_extensions_json():
    """
    Verifica o arquivo .vscode/extensions.json para ver as extensões recomendadas.
    Retorna informações sobre o que está recomendado.
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
    """Imprime instruções manuais para verificar extensões."""
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
    print("   - 'Instalado' (instalado) - botão verde com check")
    print("   - 'Instalar' (precisa instalar) - botão azul Install")
    print("\n5. Reporte o status encontrado.")
    print("="*60 + "\n")

def main():
    """Função principal para verificar extensões e reportar status."""
    print("="*60)
    print("Passo 1: Verificando extensões do GitHub Copilot")
    print("="*60 + "\n")
    
    # Tenta método CLI primeiro
    results = check_vscode_extensions_via_cli()
    
    if results is not None:
        # Método CLI funcionou
        print("✓ Verificação automática via VS Code CLI\n")
        print("encontrei:")
        for ext_name, status in results.items():
            status_icon = "✓" if status == "Instalado" else "⚠"
            print(f"  {status_icon} {ext_name}: {status}")
        
        all_installed = all(status == "Instalado" for status in results.values())
        
        if all_installed:
            print("\n✓ Todas as extensões estão instaladas!")
        else:
            print("\n⚠ Algumas extensões precisam ser instaladas.")
        
        print("\n" + "="*60)
        print("Próximo passo: Sign in (aguardando comando...)")
        print("="*60)
        
        return 0 if all_installed else 1
    else:
        # CLI não disponível, verifica extensions.json e fornece instruções manuais
        print("⚠ VS Code CLI não disponível neste ambiente.\n")
        
        # Verifica o que está recomendado em extensions.json
        recommendations = check_extensions_json()
        if recommendations:
            print("Extensões recomendadas em .vscode/extensions.json:")
            for rec in recommendations:
                print(f"  - {rec}")
            print()
        
        # Fornece instruções manuais
        print_manual_instructions()
        
        print("Por favor, execute as instruções manuais acima e reporte:")
        print("encontrei: [status das extensões]")
        print("\nExemplo de resposta esperada:")
        print("  encontrei:")
        print("  - GitHub Copilot: Instalado")
        print("  - GitHub Copilot Chat: Instalado")
        print("\nOU")
        print("  encontrei:")
        print("  - GitHub Copilot: Instalar")
        print("  - GitHub Copilot Chat: Instalar")
        
        return 2  # Código de saída 2 indica que verificação manual é necessária

if __name__ == "__main__":
    sys.exit(main())
