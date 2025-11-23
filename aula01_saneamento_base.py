#!/usr/bin/env python3
"""
Aula 01: Saneamento e Validação de Números CNJ

Este script demonstra a validação de números de processo no formato CNJ
(Conselho Nacional de Justiça) conforme a Resolução CNJ nº 65/2008.

Formato CNJ: NNNNNNN-DD.AAAA.J.TR.OOOO
Onde:
- NNNNNNN: Número sequencial do processo (7 dígitos)
- DD: Dígito verificador (2 dígitos)
- AAAA: Ano de ajuizamento (4 dígitos)
- J: Segmento do Poder Judiciário (1 dígito)
- TR: Tribunal (2 dígitos)
- OOOO: Unidade de origem (4 dígitos)

O algoritmo de validação utiliza módulo 97.

Nota: Este é um script educacional standalone. A lógica de validação também está
disponível em tests/test_cnj_validation.py, mas foi replicada aqui para que o
script possa ser executado de forma independente sem dependências adicionais.
"""

from typing import List, Tuple


def is_valid_cnj(cnj: str) -> bool:
    """
    Valida um número de processo no formato CNJ (NNNNNNN-DD.AAAA.J.TR.OOOO).
    Referência: Resolução CNJ nº 65/2008.
    
    Args:
        cnj: String contendo o número CNJ (pode conter ou não formatação)
    
    Returns:
        bool: True se o número CNJ é válido, False caso contrário
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


def format_cnj(cnj: str) -> str:
    """
    Formata um número CNJ com os separadores padrão.
    
    Args:
        cnj: String contendo apenas os 20 dígitos do CNJ
    
    Returns:
        str: Número CNJ formatado (NNNNNNN-DD.AAAA.J.TR.OOOO)
    """
    raw = "".join(filter(str.isdigit, cnj))
    
    if len(raw) != 20:
        return cnj
    
    # NNNNNNN-DD.AAAA.J.TR.OOOO
    formatted = f"{raw[0:7]}-{raw[7:9]}.{raw[9:13]}.{raw[13:14]}.{raw[14:16]}.{raw[16:20]}"
    return formatted


def calculate_check_digit(base: str) -> str:
    """
    Calcula o dígito verificador para um número CNJ sem os dígitos verificadores.
    
    Args:
        base: String com NNNNNNN + AAAA + J + TR + OOOO (18 dígitos ou mais)
    
    Returns:
        str: Dígito verificador de 2 dígitos
    """
    # Sanitize input - remove non-digit characters
    base = "".join(filter(str.isdigit, base))
    
    if len(base) != 18:
        raise ValueError("Base deve conter exatamente 18 dígitos")
    
    # Para calcular o dígito verificador:
    # 1. Concatenar base + "00"
    # 2. Calcular resto = (base + "00") % 97
    # 3. DD = 98 - resto
    
    base_num = int(base + "00")
    resto = base_num % 97
    dd = 98 - resto
    
    return f"{dd:02d}"


def validate_and_display_results(test_cases: List[Tuple[str, bool, str]]):
    """
    Valida uma lista de números CNJ e exibe os resultados.
    
    Args:
        test_cases: Lista de tuplas (cnj, esperado, descrição)
    """
    print("=" * 80)
    print("VALIDAÇÃO DE NÚMEROS CNJ")
    print("=" * 80)
    print()
    
    for cnj, expected, description in test_cases:
        result = is_valid_cnj(cnj)
        status = "✓ VÁLIDO" if result else "✗ INVÁLIDO"
        match = "✓" if result == expected else "✗ ERRO"
        
        formatted = format_cnj(cnj)
        
        print(f"{match} {status}: {formatted}")
        print(f"   Descrição: {description}")
        print(f"   Input: {cnj}")
        print()


def demonstrate_cnj_validation():
    """
    Demonstra o funcionamento da validação CNJ com exemplos práticos.
    """
    print("\n" + "=" * 80)
    print("AULA 01: SANEAMENTO E VALIDAÇÃO DE NÚMEROS CNJ")
    print("=" * 80)
    print()
    print("Este script demonstra como validar números de processo no padrão CNJ.")
    print("Formato: NNNNNNN-DD.AAAA.J.TR.OOOO")
    print()
    
    # Casos de teste
    test_cases = [
        # (número CNJ, esperado válido?, descrição)
        ("0000001-79.2023.8.26.0001", True, "CNJ válido - Formato completo com pontuação"),
        ("00000017920238260001", True, "CNJ válido - Apenas dígitos"),
        ("0000001-80.2023.8.26.0001", False, "CNJ inválido - Dígito verificador incorreto (80 em vez de 79)"),
        ("12345", False, "CNJ inválido - Tamanho incorreto (muito curto)"),
        ("0000002-24.2024.8.26.0100", True, "CNJ válido - Outro exemplo válido"),
        ("0000002-27.2024.8.26.0100", False, "CNJ inválido - Dígito verificador incorreto"),
    ]
    
    validate_and_display_results(test_cases)
    
    # Demonstração de cálculo de dígito verificador
    print("=" * 80)
    print("CÁLCULO DE DÍGITO VERIFICADOR")
    print("=" * 80)
    print()
    
    # Base sem dígito verificador: NNNNNNN + AAAA + J + TR + OOOO
    bases = [
        ("000000120238260001", "Base: 0000001 + 2023 + 8 + 26 + 0001"),
        ("000000220248260100", "Base: 0000002 + 2024 + 8 + 26 + 0100"),
    ]
    
    for base, description in bases:
        dd = calculate_check_digit(base)
        n_seq = base[0:7]
        ano = base[7:11]
        j = base[11:12]
        tr = base[12:14]
        oooo = base[14:18]
        
        full_cnj = f"{n_seq}{dd}{ano}{j}{tr}{oooo}"
        formatted = format_cnj(full_cnj)
        
        print(f"{description}")
        print(f"Dígito verificador calculado: {dd}")
        print(f"CNJ completo: {formatted}")
        print(f"Validação: {'✓ VÁLIDO' if is_valid_cnj(formatted) else '✗ INVÁLIDO'}")
        print()
    
    # Estatísticas
    print("=" * 80)
    print("RESUMO")
    print("=" * 80)
    print()
    valid_count = sum(1 for _, expected, _ in test_cases if expected)
    invalid_count = len(test_cases) - valid_count
    print(f"Total de casos testados: {len(test_cases)}")
    print(f"Casos válidos esperados: {valid_count}")
    print(f"Casos inválidos esperados: {invalid_count}")
    print()
    
    # Verificar todos os casos
    all_correct = all(
        is_valid_cnj(cnj) == expected
        for cnj, expected, _ in test_cases
    )
    
    if all_correct:
        print("✓ Todos os casos foram validados corretamente!")
    else:
        print("✗ Alguns casos apresentaram resultados inesperados.")
    
    print()


if __name__ == "__main__":
    demonstrate_cnj_validation()
