#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes Automatizados para Projeto Jurimetria
============================================

Conjunto de testes para validar funcionalidades principais.

Executar com: pytest test_jurimetria.py -v
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Importar funções do script principal
sys.path.insert(0, str(Path(__file__).parent))
from jurimetria_completa import gerar_dados_simulados
from validacao_dados import ValidadorDadosJudiciais


class TestGeracaoDados:
    """Testes para geração de dados simulados."""
    
    def test_gerar_dados_simulados_retorna_dataframe(self):
        """Verifica se a função retorna um DataFrame."""
        df = gerar_dados_simulados(n_processos=10)
        assert isinstance(df, pd.DataFrame)
    
    def test_gerar_dados_simulados_numero_correto_linhas(self):
        """Verifica se o número de processos gerados está correto."""
        n = 50
        df = gerar_dados_simulados(n_processos=n)
        assert len(df) == n
    
    def test_gerar_dados_simulados_colunas_obrigatorias(self):
        """Verifica se todas as colunas obrigatórias estão presentes."""
        df = gerar_dados_simulados(n_processos=10)
        colunas_obrigatorias = [
            'processo_id', 'tribunal', 'juiz', 'classe',
            'valor_causa', 'tempo_tramitacao_dias', 'resultado',
            'status', 'data_distribuicao'
        ]
        for col in colunas_obrigatorias:
            assert col in df.columns
    
    def test_gerar_dados_simulados_sem_nulos(self):
        """Verifica se não há valores nulos em colunas críticas."""
        df = gerar_dados_simulados(n_processos=10)
        assert df['processo_id'].notna().all()
        assert df['resultado'].notna().all()
        assert df['tempo_tramitacao_dias'].notna().all()
    
    def test_gerar_dados_simulados_ids_unicos(self):
        """Verifica se os IDs de processo são únicos."""
        df = gerar_dados_simulados(n_processos=10)
        assert df['processo_id'].is_unique
    
    def test_gerar_dados_simulados_valores_positivos(self):
        """Verifica se valores numéricos são positivos."""
        df = gerar_dados_simulados(n_processos=10)
        assert (df['valor_causa'] > 0).all()
        assert (df['tempo_tramitacao_dias'] > 0).all()
    
    def test_gerar_dados_simulados_resultado_binario(self):
        """Verifica se resultado é binário (0 ou 1)."""
        df = gerar_dados_simulados(n_processos=10)
        assert df['resultado'].isin([0, 1]).all()
    
    def test_gerar_dados_simulados_status_binario(self):
        """Verifica se status é binário (0 ou 1)."""
        df = gerar_dados_simulados(n_processos=10)
        assert df['status'].isin([0, 1]).all()
    
    def test_gerar_dados_simulados_reproducibilidade(self):
        """Verifica se dados são reproduzíveis com mesmo seed."""
        df1 = gerar_dados_simulados(n_processos=10, seed=123)
        df2 = gerar_dados_simulados(n_processos=10, seed=123)
        pd.testing.assert_frame_equal(df1, df2)


class TestValidadorDados:
    """Testes para validação de dados."""
    
    @pytest.fixture
    def dados_validos(self):
        """Fixture com dados válidos."""
        return gerar_dados_simulados(n_processos=20)
    
    @pytest.fixture
    def dados_com_erros(self):
        """Fixture com dados contendo erros."""
        df = gerar_dados_simulados(n_processos=20)
        # Introduzir erros
        df.loc[0, 'valor_causa'] = -100  # Valor negativo
        df.loc[1, 'resultado'] = 5  # Valor inválido
        df.loc[2, 'processo_id'] = df.loc[3, 'processo_id']  # Duplicata
        return df
    
    def test_validador_dados_validos(self, dados_validos):
        """Testa validação com dados válidos."""
        validador = ValidadorDadosJudiciais(dados_validos)
        validador.executar_validacao_completa()
        assert len(validador.erros) == 0
    
    def test_validador_detecta_valores_negativos(self, dados_com_erros):
        """Testa se validador detecta valores negativos."""
        validador = ValidadorDadosJudiciais(dados_com_erros)
        validador.validar_valores_numericos()
        assert len(validador.erros) > 0
        assert any('negativo' in erro.lower() for erro in validador.erros)
    
    def test_validador_detecta_valores_categoricos_invalidos(self, dados_com_erros):
        """Testa se validador detecta valores categóricos inválidos."""
        validador = ValidadorDadosJudiciais(dados_com_erros)
        validador.validar_categorias()
        assert len(validador.erros) > 0
    
    def test_validador_detecta_duplicatas(self, dados_com_erros):
        """Testa se validador detecta duplicatas."""
        validador = ValidadorDadosJudiciais(dados_com_erros)
        validador.validar_duplicatas()
        assert len(validador.erros) > 0
        assert any('duplicado' in erro.lower() for erro in validador.erros)
    
    def test_validador_colunas_obrigatorias_faltantes(self):
        """Testa detecção de colunas faltantes."""
        df = pd.DataFrame({'processo_id': [1, 2, 3]})
        validador = ValidadorDadosJudiciais(df)
        validador.validar_colunas_obrigatorias()
        assert len(validador.erros) > 0


class TestAnaliseDescritiva:
    """Testes para análise descritiva."""
    
    def test_estatisticas_basicas(self):
        """Testa cálculo de estatísticas básicas."""
        df = gerar_dados_simulados(n_processos=100)
        
        # Verificar se estatísticas podem ser calculadas
        assert df['tempo_tramitacao_dias'].mean() > 0
        assert df['tempo_tramitacao_dias'].median() > 0
        assert df['tempo_tramitacao_dias'].std() > 0
    
    def test_taxa_procedencia(self):
        """Testa cálculo de taxa de procedência."""
        df = gerar_dados_simulados(n_processos=100)
        taxa = df['resultado'].mean()
        
        # Taxa deve estar entre 0 e 1
        assert 0 <= taxa <= 1
    
    def test_distribuicao_classes(self):
        """Testa distribuição de classes processuais."""
        df = gerar_dados_simulados(n_processos=100)
        distribuicao = df['classe'].value_counts()
        
        # Deve haver pelo menos uma classe
        assert len(distribuicao) > 0
        # Soma deve ser igual ao total de processos
        assert distribuicao.sum() == len(df)


class TestAnaliseComparativa:
    """Testes para análises comparativas."""
    
    def test_comparacao_tempo_tramitacao_por_classe(self):
        """Testa comparação de tempo de tramitação por classe."""
        df = gerar_dados_simulados(n_processos=100)
        agrupado = df.groupby('classe')['tempo_tramitacao_dias'].mean()
        
        # Deve haver médias para cada classe
        assert len(agrupado) > 0
        # Todas as médias devem ser positivas
        assert (agrupado > 0).all()
    
    def test_comparacao_valor_causa_por_resultado(self):
        """Testa comparação de valor da causa por resultado."""
        df = gerar_dados_simulados(n_processos=100)
        agrupado = df.groupby('resultado')['valor_causa'].mean()
        
        # Deve haver duas categorias de resultado
        assert len(agrupado) == 2
        # Todas as médias devem ser positivas
        assert (agrupado > 0).all()


class TestIntegridadeDados:
    """Testes de integridade de dados."""
    
    def test_consistencia_status_tempo(self):
        """Testa consistência entre status e tempo de tramitação."""
        df = gerar_dados_simulados(n_processos=100)
        
        # Processos encerrados (status=1) devem ter tempo > 0
        processos_encerrados = df[df['status'] == 1]
        if len(processos_encerrados) > 0:
            assert (processos_encerrados['tempo_tramitacao_dias'] > 0).all()
    
    def test_tribunais_pilotos(self):
        """Testa se os 3 tribunais pilotos estão presentes."""
        df = gerar_dados_simulados(n_processos=150)
        tribunais = df['tribunal'].unique()
        
        # Deve haver 3 tribunais pilotos
        assert len(tribunais) == 3
        # Verificar nomes esperados
        assert 'TJ-SP' in tribunais
        assert 'TJ-RJ' in tribunais
        assert 'TJ-MG' in tribunais
    
    def test_juizes_presentes(self):
        """Testa se há juízes nos dados."""
        df = gerar_dados_simulados(n_processos=100)
        juizes = df['juiz'].unique()
        
        # Deve haver pelo menos um juiz
        assert len(juizes) > 0


class TestRobustez:
    """Testes de robustez e casos extremos."""
    
    def test_dados_minimos(self):
        """Testa geração com número mínimo de processos."""
        df = gerar_dados_simulados(n_processos=1)
        assert len(df) == 1
        assert df['processo_id'].iloc[0] is not None
    
    def test_dados_grandes(self):
        """Testa geração com grande volume de dados."""
        df = gerar_dados_simulados(n_processos=1000)
        assert len(df) == 1000
        # Verificar que não há problemas de memória ou performance
        assert df['processo_id'].is_unique


# Configuração do pytest
def pytest_configure(config):
    """Configuração do pytest."""
    config.addinivalue_line(
        "markers", "slow: marca testes que são lentos"
    )


if __name__ == '__main__':
    # Executar testes
    pytest.main([__file__, '-v', '--tb=short'])
