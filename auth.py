"""
Módulo de autenticação simples baseado em token.
Simple token-based authentication module.
"""
import hashlib
import secrets
from pathlib import Path
from typing import Optional


class TokenAuth:
    """Gerenciador de autenticação por token."""
    
    def __init__(self, token_file: str = 'projeto/token'):
        """
        Inicializa o gerenciador de autenticação.
        
        Args:
            token_file: Caminho para o arquivo de token
        """
        self.token_file = Path(token_file)
        self.token_file.parent.mkdir(parents=True, exist_ok=True)
    
    def generate_token(self) -> str:
        """
        Gera um novo token seguro.
        
        Returns:
            Token gerado como string hexadecimal
        """
        token = secrets.token_hex(32)
        return token
    
    def save_token(self, token: str) -> None:
        """
        Salva o token (hash) no arquivo.
        
        Args:
            token: Token a ser salvo
        """
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        self.token_file.write_text(token_hash, encoding='utf-8')
    
    def verify_token(self, token: str) -> bool:
        """
        Verifica se o token fornecido é válido.
        
        Args:
            token: Token a ser verificado
            
        Returns:
            True se o token for válido, False caso contrário
        """
        if not self.token_file.exists():
            return False
        
        stored_hash = self.token_file.read_text(encoding='utf-8').strip()
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        return secrets.compare_digest(stored_hash, token_hash)
    
    def has_token(self) -> bool:
        """
        Verifica se existe um token salvo.
        
        Returns:
            True se existe token, False caso contrário
        """
        return self.token_file.exists() and len(self.token_file.read_text().strip()) > 0
    
    def setup_new_token(self) -> str:
        """
        Configura um novo token e o salva.
        
        Returns:
            O token gerado (deve ser guardado pelo usuário)
        """
        token = self.generate_token()
        self.save_token(token)
        return token
