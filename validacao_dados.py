#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Validação de Dados Judiciais
======================================

Este script valida a qualidade e integridade dos dados antes da análise.

Autor: Projeto Jurimetria
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys


class ValidadorDadosJudiciais:
    """Classe para validação de dados judiciais."""
    
    def __init__(self, df):
        """
        Inicializa o validador.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame com dados a validar
        """
        self.df = df
        self.erros = []
        self.avisos = []
        
    def validar_colunas_obrigatorias(self):
        """Verifica se todas as colunas obrigatórias estão presentes."""
        colunas_obrigatorias = [
            'processo_id',
            'tribunal',
            'juiz',
            'classe',
            'valor_causa',
            'tempo_tramitacao_dias',
            'resultado',
            'status'
        ]
        
        colunas_faltantes = [col for col in colunas_obrigatorias if col not in self.df.columns]
        
        if colunas_faltantes:
            self.erros.append(f"Colunas obrigatórias ausentes: {', '.join(colunas_faltantes)}")
        else:
            print("✓ Todas as colunas obrigatórias estão presentes")
            
    def validar_valores_nulos(self):
        """Verifica valores nulos em colunas críticas."""
        colunas_criticas = ['processo_id', 'resultado', 'tempo_tramitacao_dias']
        
        for col in colunas_criticas:
            if col in self.df.columns:
                n_nulos = self.df[col].isna().sum()
                if n_nulos > 0:
                    pct_nulos = (n_nulos / len(self.df)) * 100
                    self.erros.append(f"Coluna '{col}' tem {n_nulos} valores nulos ({pct_nulos:.2f}%)")
        
        if not self.erros:
            print("✓ Sem valores nulos em colunas críticas")
            
    def validar_duplicatas(self):
        """Verifica se há processos duplicados."""
        if 'processo_id' in self.df.columns:
            n_duplicatas = self.df['processo_id'].duplicated().sum()
            if n_duplicatas > 0:
                self.erros.append(f"Encontradas {n_duplicatas} IDs de processo duplicados")
            else:
                print("✓ Sem processos duplicados")
                
    def validar_valores_numericos(self):
        """Valida se valores numéricos estão em faixas razoáveis."""
        # Valor da causa
        if 'valor_causa' in self.df.columns:
            valores_negativos = (self.df['valor_causa'] < 0).sum()
            if valores_negativos > 0:
                self.erros.append(f"Encontrados {valores_negativos} valores de causa negativos")
            
            valores_zero = (self.df['valor_causa'] == 0).sum()
            if valores_zero > 0:
                pct_zero = (valores_zero / len(self.df)) * 100
                self.avisos.append(f"{valores_zero} processos com valor de causa = 0 ({pct_zero:.2f}%)")
        
        # Tempo de tramitação
        if 'tempo_tramitacao_dias' in self.df.columns:
            tempos_negativos = (self.df['tempo_tramitacao_dias'] < 0).sum()
            if tempos_negativos > 0:
                self.erros.append(f"Encontrados {tempos_negativos} tempos de tramitação negativos")
            
            tempos_muito_longos = (self.df['tempo_tramitacao_dias'] > 3650).sum()  # > 10 anos
            if tempos_muito_longos > 0:
                pct_longos = (tempos_muito_longos / len(self.df)) * 100
                self.avisos.append(f"{tempos_muito_longos} processos com tramitação > 10 anos ({pct_longos:.2f}%)")
        
        if not self.erros:
            print("✓ Valores numéricos dentro de faixas esperadas")
            
    def validar_categorias(self):
        """Valida valores categóricos."""
        # Resultado deve ser 0 ou 1
        if 'resultado' in self.df.columns:
            valores_resultado = self.df['resultado'].unique()
            valores_invalidos = [v for v in valores_resultado if v not in [0, 1]]
            if valores_invalidos:
                self.erros.append(f"Valores inválidos em 'resultado': {valores_invalidos}")
        
        # Status deve ser 0 ou 1
        if 'status' in self.df.columns:
            valores_status = self.df['status'].unique()
            valores_invalidos = [v for v in valores_status if v not in [0, 1]]
            if valores_invalidos:
                self.erros.append(f"Valores inválidos em 'status': {valores_invalidos}")
        
        if not self.erros:
            print("✓ Valores categóricos válidos")
            
    def validar_consistencia_temporal(self):
        """Valida consistência de datas."""
        if 'data_distribuicao' in self.df.columns:
            try:
                datas = pd.to_datetime(self.df['data_distribuicao'])
                
                # Verificar datas futuras
                hoje = pd.Timestamp.now()
                datas_futuras = (datas > hoje).sum()
                if datas_futuras > 0:
                    self.erros.append(f"Encontradas {datas_futuras} datas de distribuição futuras")
                
                # Verificar datas muito antigas (antes de 1990)
                data_minima = pd.Timestamp('1990-01-01')
                datas_antigas = (datas < data_minima).sum()
                if datas_antigas > 0:
                    self.avisos.append(f"{datas_antigas} processos com data anterior a 1990")
                    
                print("✓ Datas consistentes")
            except Exception as e:
                self.erros.append(f"Erro ao validar datas: {str(e)}")
                
    def validar_distribuicao_classes(self):
        """Verifica se há distribuição razoável de classes processuais."""
        if 'classe' in self.df.columns:
            distribuicao = self.df['classe'].value_counts()
            total = len(self.df)
            
            for classe, count in distribuicao.items():
                pct = (count / total) * 100
                if pct < 5:
                    self.avisos.append(f"Classe '{classe}' representa apenas {pct:.2f}% dos processos")
            
            print(f"✓ Distribuição de classes: {len(distribuicao)} classes únicas")
            
    def gerar_relatorio(self):
        """Gera relatório de validação."""
        print("\n" + "="*60)
        print("RELATÓRIO DE VALIDAÇÃO DE DADOS")
        print("="*60)
        print(f"\nTotal de registros: {len(self.df)}")
        print(f"Total de colunas: {len(self.df.columns)}")
        
        if self.erros:
            print(f"\n❌ ERROS ENCONTRADOS ({len(self.erros)}):")
            for i, erro in enumerate(self.erros, 1):
                print(f"  {i}. {erro}")
        else:
            print("\n✓ Nenhum erro crítico encontrado")
        
        if self.avisos:
            print(f"\n⚠️  AVISOS ({len(self.avisos)}):")
            for i, aviso in enumerate(self.avisos, 1):
                print(f"  {i}. {aviso}")
        else:
            print("\n✓ Nenhum aviso")
        
        print("\n" + "="*60)
        
        if self.erros:
            print("\n❌ VALIDAÇÃO FALHOU - Corrija os erros antes de prosseguir")
            return False
        else:
            print("\n✅ VALIDAÇÃO BEM-SUCEDIDA - Dados prontos para análise")
            return True
            
    def executar_validacao_completa(self):
        """Executa todas as validações."""
        print("\n🔍 Iniciando validação de dados...\n")
        
        self.validar_colunas_obrigatorias()
        self.validar_valores_nulos()
        self.validar_duplicatas()
        self.validar_valores_numericos()
        self.validar_categorias()
        self.validar_consistencia_temporal()
        self.validar_distribuicao_classes()
        
        return self.gerar_relatorio()


def main():
    """Função principal."""
    # Tentar carregar dados
    data_dir = Path(__file__).parent / 'data'
    
    # Procurar por arquivos de dados
    arquivos_csv = list(data_dir.glob('*.csv'))
    
    if not arquivos_csv:
        print("❌ Nenhum arquivo CSV encontrado em data/")
        print("\nGere dados primeiro executando:")
        print("  python3 jurimetria_completa.py")
        sys.exit(1)
    
    # Usar o primeiro arquivo encontrado
    arquivo_dados = arquivos_csv[0]
    print(f"📂 Carregando dados de: {arquivo_dados}")
    
    try:
        df = pd.read_csv(arquivo_dados)
        print(f"✓ Dados carregados: {len(df)} registros, {len(df.columns)} colunas")
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        sys.exit(1)
    
    # Executar validação
    validador = ValidadorDadosJudiciais(df)
    sucesso = validador.executar_validacao_completa()
    
    # Retornar código de saída apropriado
    sys.exit(0 if sucesso else 1)


if __name__ == '__main__':
    main()
