"""
Script de validação CNJ para números de processos
Autor: Projeto Jurimetria
"""

import re
from typing import Tuple, List
import pandas as pd


class ValidadorCNJ:
    """Validador de números de processos conforme padrão CNJ"""
    
    @staticmethod
    def calcular_digito_verificador(numero_base: str) -> str:
        """
        Calcula o dígito verificador conforme Resolução CNJ 65/2008
        
        Args:
            numero_base: NNNNNNNAAAAJTROOOO (sem o dígito verificador)
        
        Returns:
            Dígito verificador (2 dígitos)
        """
        # Número base deve ter 18 dígitos
        if len(numero_base) != 18:
            raise ValueError("Número base deve ter 18 dígitos")
        
        # Converter para inteiro e calcular resto da divisão por 97
        numero_int = int(numero_base)
        resto = numero_int % 97
        digito = 98 - resto
        
        return str(digito).zfill(2)
    
    @staticmethod
    def validar_formato(numero_processo: str) -> Tuple[bool, str]:
        """
        Valida o formato do número do processo
        
        Args:
            numero_processo: Número do processo
        
        Returns:
            Tupla (válido, mensagem)
        """
        # Remover pontuação para validação
        numero_limpo = re.sub(r'[.\-]', '', numero_processo)
        
        # Deve ter 20 dígitos
        if len(numero_limpo) != 20:
            return False, f"Número deve ter 20 dígitos (tem {len(numero_limpo)})"
        
        # Validar formato: NNNNNNNDDAAAAJTROOOO
        padrao = r'^(\d{7})(\d{2})(\d{4})(\d{1})(\d{2})(\d{4})$'
        match = re.match(padrao, numero_limpo)
        
        if not match:
            return False, "Formato inválido"
        
        sequencial, dv, ano, segmento, tribunal, origem = match.groups()
        
        # Validar ano (deve ser >= 1900)
        ano_int = int(ano)
        if ano_int < 1900 or ano_int > 2100:
            return False, f"Ano inválido: {ano}"
        
        # Validar segmento da justiça (1-9)
        segmento_int = int(segmento)
        if segmento_int < 1 or segmento_int > 9:
            return False, f"Segmento inválido: {segmento}"
        
        # Validar dígito verificador
        numero_base = sequencial + ano + segmento + tribunal + origem
        dv_calculado = ValidadorCNJ.calcular_digito_verificador(numero_base)
        
        if dv != dv_calculado:
            return False, f"Dígito verificador incorreto. Esperado: {dv_calculado}, Encontrado: {dv}"
        
        return True, "Número válido"
    
    @staticmethod
    def formatar_numero(numero_processo: str) -> str:
        """
        Formata o número do processo no padrão CNJ
        
        Args:
            numero_processo: Número do processo (com ou sem formatação)
        
        Returns:
            Número formatado: NNNNNNN-DD.AAAA.J.TR.OOOO
        """
        # Remover formatação existente
        numero_limpo = re.sub(r'[.\-]', '', numero_processo)
        
        if len(numero_limpo) != 20:
            raise ValueError("Número deve ter 20 dígitos")
        
        # Aplicar formatação
        sequencial = numero_limpo[0:7]
        dv = numero_limpo[7:9]
        ano = numero_limpo[9:13]
        segmento = numero_limpo[13:14]
        tribunal = numero_limpo[14:16]
        origem = numero_limpo[16:20]
        
        return f"{sequencial}-{dv}.{ano}.{segmento}.{tribunal}.{origem}"
    
    @staticmethod
    def extrair_componentes(numero_processo: str) -> dict:
        """
        Extrai os componentes do número do processo
        
        Args:
            numero_processo: Número do processo
        
        Returns:
            Dicionário com componentes do número
        """
        numero_limpo = re.sub(r'[.\-]', '', numero_processo)
        
        if len(numero_limpo) != 20:
            raise ValueError("Número deve ter 20 dígitos")
        
        segmentos_justica = {
            '1': 'Supremo Tribunal Federal',
            '2': 'Conselho Nacional de Justiça',
            '3': 'Superior Tribunal de Justiça',
            '4': 'Justiça Federal',
            '5': 'Justiça do Trabalho',
            '6': 'Justiça Eleitoral',
            '7': 'Justiça Militar da União',
            '8': 'Justiça dos Estados e do Distrito Federal',
            '9': 'Justiça Militar Estadual'
        }
        
        return {
            'numero_sequencial': numero_limpo[0:7],
            'digito_verificador': numero_limpo[7:9],
            'ano_ajuizamento': numero_limpo[9:13],
            'segmento_justica': numero_limpo[13:14],
            'segmento_justica_nome': segmentos_justica.get(numero_limpo[13:14], 'Desconhecido'),
            'tribunal': numero_limpo[14:16],
            'vara_origem': numero_limpo[16:20]
        }


def testar_validacao():
    """Função de teste para validação CNJ"""
    
    print("=" * 80)
    print("TESTE DE VALIDAÇÃO CNJ")
    print("=" * 80)
    print()
    
    # Casos de teste
    casos_teste = [
        "0000001-01.2024.8.00.0001",  # Exemplo fictício
        "1234567-89.2023.5.15.0001",  # Exemplo fictício
        "0000001-01.2024.8.00.001",   # Inválido (faltam dígitos)
        "0000001-99.2024.8.00.0001",  # Inválido (DV incorreto)
        "0000001-01.1800.8.00.0001",  # Inválido (ano incorreto)
    ]
    
    resultados = []
    
    for numero in casos_teste:
        valido, mensagem = ValidadorCNJ.validar_formato(numero)
        
        print(f"Número: {numero}")
        print(f"Status: {'✓ VÁLIDO' if valido else '✗ INVÁLIDO'}")
        print(f"Mensagem: {mensagem}")
        
        if valido:
            try:
                componentes = ValidadorCNJ.extrair_componentes(numero)
                print(f"Componentes:")
                for chave, valor in componentes.items():
                    print(f"  - {chave}: {valor}")
                
                formatado = ValidadorCNJ.formatar_numero(numero)
                print(f"Formatado: {formatado}")
            except Exception as e:
                print(f"Erro ao extrair componentes: {e}")
        
        print("-" * 80)
        
        resultados.append({
            'numero': numero,
            'valido': valido,
            'mensagem': mensagem
        })
    
    # Criar DataFrame com resultados
    df = pd.DataFrame(resultados)
    
    print("\nRESUMO DOS TESTES")
    print(df.to_string(index=False))
    
    # Salvar resultados
    df.to_csv('resultados/validacao_cnj_teste.csv', index=False)
    print("\nResultados salvos em: resultados/validacao_cnj_teste.csv")


def validar_arquivo(caminho_arquivo: str, coluna_numero: str = 'numero_processo'):
    """
    Valida números de processos em um arquivo
    
    Args:
        caminho_arquivo: Caminho para o arquivo (CSV ou Excel)
        coluna_numero: Nome da coluna com números de processos
    """
    # Ler arquivo
    if caminho_arquivo.endswith('.csv'):
        df = pd.read_csv(caminho_arquivo)
    elif caminho_arquivo.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(caminho_arquivo)
    else:
        raise ValueError("Formato de arquivo não suportado. Use CSV ou Excel.")
    
    # Validar cada número
    resultados = []
    
    for idx, numero in enumerate(df[coluna_numero]):
        valido, mensagem = ValidadorCNJ.validar_formato(str(numero))
        resultados.append({
            'linha': idx + 1,
            'numero': numero,
            'valido': valido,
            'mensagem': mensagem
        })
    
    df_resultados = pd.DataFrame(resultados)
    
    # Estatísticas
    total = len(df_resultados)
    validos = df_resultados['valido'].sum()
    invalidos = total - validos
    
    print(f"\nESTATÍSTICAS DE VALIDAÇÃO")
    print(f"Total de processos: {total}")
    print(f"Válidos: {validos} ({validos/total*100:.1f}%)")
    print(f"Inválidos: {invalidos} ({invalidos/total*100:.1f}%)")
    
    # Salvar resultados
    output_file = 'resultados/validacao_arquivo.xlsx'
    df_resultados.to_excel(output_file, index=False)
    print(f"\nResultados salvos em: {output_file}")
    
    return df_resultados


if __name__ == '__main__':
    # Executar testes
    testar_validacao()
