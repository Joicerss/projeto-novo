#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Planilha Modelo (Template)
=====================================

Gera uma planilha Excel modelo para entrada de dados judiciais.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


def criar_template_excel():
    """Cria planilha modelo para entrada de dados."""
    
    # Dados de exemplo
    exemplos = []
    for i in range(5):
        exemplos.append({
            'processo_id': f'PROC-EXEMPLO-{i+1:03d}',
            'tribunal': 'TJ-SP',
            'juiz': 'Nome do Juiz',
            'classe': 'Cível',
            'valor_causa': 50000.00,
            'tempo_tramitacao_dias': 365,
            'resultado': 1,
            'status': 1,
            'data_distribuicao': (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
            'observacoes': 'Campo opcional para anotações'
        })
    
    df = pd.DataFrame(exemplos)
    
    # Criar arquivo Excel
    output_file = Path(__file__).parent / 'data' / 'template_dados.xlsx'
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Aba principal com dados
        df.to_excel(writer, sheet_name='Dados', index=False)
        
        # Aba de instruções
        instrucoes = pd.DataFrame({
            'Coluna': [
                'processo_id',
                'tribunal',
                'juiz',
                'classe',
                'valor_causa',
                'tempo_tramitacao_dias',
                'resultado',
                'status',
                'data_distribuicao',
                'observacoes'
            ],
            'Descrição': [
                'Identificador único do processo (obrigatório)',
                'Sigla do tribunal (ex: TJ-SP, TJ-RJ, TJ-MG)',
                'Nome do juiz responsável',
                'Classe processual (ex: Cível, Trabalhista, Criminal)',
                'Valor da causa em reais (número decimal)',
                'Tempo de tramitação em dias (número inteiro)',
                'Resultado: 0 = Improcedente, 1 = Procedente',
                'Status: 0 = Em andamento, 1 = Encerrado',
                'Data de distribuição do processo (formato: AAAA-MM-DD)',
                'Campo livre para anotações (opcional)'
            ],
            'Tipo': [
                'Texto',
                'Texto',
                'Texto',
                'Texto',
                'Número',
                'Número',
                'Número (0 ou 1)',
                'Número (0 ou 1)',
                'Data',
                'Texto'
            ],
            'Obrigatório': [
                'Sim',
                'Sim',
                'Sim',
                'Sim',
                'Sim',
                'Sim',
                'Sim',
                'Sim',
                'Não',
                'Não'
            ]
        })
        instrucoes.to_excel(writer, sheet_name='Instruções', index=False)
        
        # Aba de valores válidos
        valores_validos = pd.DataFrame({
            'Tribunais Válidos': ['TJ-SP', 'TJ-RJ', 'TJ-MG', 'TJ-RS', 'TJ-BA', '(adicionar conforme necessário)'],
            'Classes Válidas': ['Cível', 'Trabalhista', 'Criminal', 'Família', 'Tributário', '(adicionar conforme necessário)'],
            'Resultado': ['0 = Improcedente', '1 = Procedente', '', '', '', ''],
            'Status': ['0 = Em andamento', '1 = Encerrado', '', '', '', '']
        })
        valores_validos.to_excel(writer, sheet_name='Valores Válidos', index=False)
    
    print(f"✓ Template criado: {output_file}")
    return output_file


if __name__ == '__main__':
    criar_template_excel()
