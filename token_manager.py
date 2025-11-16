"""
Script para gerenciar tokens de autenticação.
Script to manage authentication tokens.
"""
import sys
from auth import TokenAuth


def main():
    """Função principal para gerenciamento de tokens."""
    auth = TokenAuth()
    
    if len(sys.argv) < 2:
        print("Uso: python token_manager.py [gerar|verificar]")
        print("Usage: python token_manager.py [generate|verify]")
        print()
        print("Comandos / Commands:")
        print("  gerar / generate  - Gera um novo token")
        print("  verificar / verify <token> - Verifica um token")
        sys.exit(1)
    
    comando = sys.argv[1].lower()
    
    if comando in ['gerar', 'generate']:
        if auth.has_token():
            resposta = input("Já existe um token. Deseja substituir? (s/n): ")
            if resposta.lower() not in ['s', 'y', 'yes', 'sim']:
                print("Operação cancelada.")
                sys.exit(0)
        
        token = auth.setup_new_token()
        print("\n" + "=" * 60)
        print("NOVO TOKEN GERADO:")
        print(token)
        print("=" * 60)
        print("\n⚠️  IMPORTANTE: Guarde este token em local seguro!")
        print("   Ele será necessário para autenticação.")
        print("   Este token não será mostrado novamente.")
        print("\n⚠️  IMPORTANT: Save this token in a secure location!")
        print("   It will be required for authentication.")
        print("   This token will not be shown again.")
        
    elif comando in ['verificar', 'verify']:
        if len(sys.argv) < 3:
            print("Erro: Token não fornecido")
            print("Error: Token not provided")
            print("Uso: python token_manager.py verificar <token>")
            sys.exit(1)
        
        token_fornecido = sys.argv[2]
        
        if not auth.has_token():
            print("❌ Nenhum token configurado no sistema")
            print("❌ No token configured in the system")
            sys.exit(1)
        
        if auth.verify_token(token_fornecido):
            print("✅ Token válido!")
            print("✅ Valid token!")
        else:
            print("❌ Token inválido!")
            print("❌ Invalid token!")
            sys.exit(1)
    
    else:
        print(f"Comando desconhecido: {comando}")
        print(f"Unknown command: {comando}")
        sys.exit(1)


if __name__ == '__main__':
    main()
