"""
Testes básicos para o módulo de autenticação.
Basic tests for the authentication module.
"""
import os
import tempfile
from pathlib import Path
from auth import TokenAuth


def test_token_generation():
    """Testa a geração de tokens."""
    auth = TokenAuth()
    token = auth.generate_token()
    
    # Token deve ter 64 caracteres hexadecimais
    assert len(token) == 64, f"Token deve ter 64 caracteres, tem {len(token)}"
    assert all(c in '0123456789abcdef' for c in token), "Token deve ser hexadecimal"
    print("✅ Teste de geração de token passou")


def test_token_save_and_verify():
    """Testa o salvamento e verificação de tokens."""
    # Usar arquivo temporário
    with tempfile.TemporaryDirectory() as tmpdir:
        token_file = Path(tmpdir) / "test_token"
        auth = TokenAuth(str(token_file))
        
        # Gerar e salvar token
        token = auth.setup_new_token()
        
        # Verificar que o arquivo foi criado
        assert auth.has_token(), "Token deveria existir"
        
        # Verificar token correto
        assert auth.verify_token(token), "Token correto deveria ser válido"
        
        # Verificar token incorreto
        assert not auth.verify_token("wrong_token"), "Token incorreto deveria ser inválido"
        
        # Verificar token vazio
        assert not auth.verify_token(""), "Token vazio deveria ser inválido"
        
        print("✅ Teste de salvamento e verificação passou")


def test_token_replacement():
    """Testa a substituição de tokens."""
    with tempfile.TemporaryDirectory() as tmpdir:
        token_file = Path(tmpdir) / "test_token"
        auth = TokenAuth(str(token_file))
        
        # Criar primeiro token
        token1 = auth.setup_new_token()
        assert auth.verify_token(token1), "Primeiro token deveria ser válido"
        
        # Criar segundo token (substituir)
        token2 = auth.setup_new_token()
        assert auth.verify_token(token2), "Segundo token deveria ser válido"
        assert not auth.verify_token(token1), "Primeiro token não deveria mais ser válido"
        
        print("✅ Teste de substituição de token passou")


def test_no_token_file():
    """Testa comportamento quando não há arquivo de token."""
    with tempfile.TemporaryDirectory() as tmpdir:
        token_file = Path(tmpdir) / "nonexistent_token"
        auth = TokenAuth(str(token_file))
        
        # Não deveria ter token
        assert not auth.has_token(), "Não deveria ter token"
        
        # Verificação deveria falhar
        assert not auth.verify_token("any_token"), "Verificação deveria falhar sem token configurado"
        
        print("✅ Teste de arquivo inexistente passou")


def test_different_tokens_are_unique():
    """Testa que tokens gerados são únicos."""
    auth = TokenAuth()
    tokens = [auth.generate_token() for _ in range(100)]
    
    # Todos os tokens devem ser diferentes
    assert len(set(tokens)) == 100, "Tokens gerados devem ser únicos"
    
    print("✅ Teste de unicidade de tokens passou")


if __name__ == '__main__':
    print("Executando testes de autenticação...\n")
    print("Running authentication tests...\n")
    
    try:
        test_token_generation()
        test_token_save_and_verify()
        test_token_replacement()
        test_no_token_file()
        test_different_tokens_are_unique()
        
        print("\n" + "=" * 60)
        print("✅ Todos os testes passaram!")
        print("✅ All tests passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ Teste falhou: {e}")
        print(f"❌ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print(f"❌ Unexpected error: {e}")
        exit(1)
