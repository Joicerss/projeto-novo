import pytest
import re

def is_valid_cnj(cnj: str) -> bool:
    """
    Valida um número de processo no formato CNJ (NNNNNNN-DD.AAAA.J.TR.OOOO).
    Referência: Resolução CNJ nº 65/2008.
    """
    # Remove caracteres não numéricos
    raw = "".join(filter(str.isdigit, cnj))
    
    if len(raw) != 20:
        return False
        
    # Formato: NNNNNNN DD AAAA J TR OOOO
    # N: Número sequencial
    # D: Dígito verificador
    # A: Ano
    # J: Órgão do Judiciário
    # T: Tribunal
    # O: Unidade de origem
    
    # O algoritmo calcula o módulo 97.
    # Para validar, movemos os dígitos verificadores (DD) para o final.
    # Formato original: NNNNNNN DD AAAA J TR OOOO
    # Formato para validação: NNNNNNN AAAA J TR OOOO DD
    
    # Extrair componentes
    # NNNNNNN (7)
    n_seq = raw[0:7]
    # DD (2)
    dd = raw[7:9]
    # AAAA (4)
    ano = raw[9:13]
    # J (1)
    j = raw[13:14]
    # TR (2)
    tr = raw[14:16]
    # OOOO (4)
    oooo = raw[16:20]
    
    # Reorganizar
    num_validacao = n_seq + ano + j + tr + oooo + dd
    
    try:
        val = int(num_validacao)
        return (val % 97) == 1
    except ValueError:
        return False

def test_cnj_format_validation():
    # Exemplo válido construído anteriormente:
    # Base: 0000001 2023 8 26 0001
    # DD calculado foi 79.
    # CNJ: 0000001-79.2023.8.26.0001
    
    valid_cnj = "0000001-79.2023.8.26.0001"
    assert is_valid_cnj(valid_cnj), f"O CNJ {valid_cnj} deveria ser válido"

def test_invalid_cnj():
    # Tamanho errado
    assert not is_valid_cnj("12345")
    # Dígito verificador errado
    invalid_cnj = "0000001-80.2023.8.26.0001"
    assert not is_valid_cnj(invalid_cnj)

def test_pipeline_sample_cnj():
    """
    Verifica se os processos no arquivo de exemplo (se houver) são válidos ou se a função lida com eles.
    """
    # Testa com string sem pontuação (mas na ordem original NNNNNNNDDAAAAJTROOOO)
    # O validador deve reorganizar internamente.
    # Exemplo válido: 0000001-79.2023.8.26.0001 -> 00000017920238260001
    assert is_valid_cnj("00000017920238260001")
