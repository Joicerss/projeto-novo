#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Principal de Análise Jurimetrica
=======================================

Este script realiza análises estatísticas completas de dados judiciais,
incluindo análises descritivas, preditivas e de sobrevivência.

Autor: Projeto Jurimetria
Data: 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
from datetime import datetime
import json

# Machine Learning
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

# Survival Analysis
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import multivariate_logrank_test

# Statistical Tests
from scipy import stats

warnings.filterwarnings('ignore')

# Configurações
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)

# Diretórios
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
OUTPUT_DIR = BASE_DIR / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)


def gerar_dados_simulados(n_processos=150, seed=42):
    """
    Gera dados judiciais simulados para demonstração.
    
    Em produção, esta função seria substituída por leitura de dados reais
    do DataJud ou de outras fontes.
    
    Parameters
    ----------
    n_processos : int
        Número de processos a simular
    seed : int
        Seed para reprodutibilidade
    
    Returns
    -------
    pd.DataFrame
        DataFrame com dados simulados
    """
    np.random.seed(seed)
    
    # Juízes dos 3 tribunais pilotos
    juizes = ['Juiz A', 'Juiz B', 'Juiz C'] * (n_processos // 3)
    juizes += ['Juiz A'] * (n_processos - len(juizes))
    
    # Classes processuais
    classes = np.random.choice(
        ['Cível', 'Trabalhista', 'Criminal'],
        size=n_processos,
        p=[0.5, 0.3, 0.2]
    )
    
    # Valores da causa (em reais)
    valores_causa = np.random.lognormal(mean=10, sigma=1.5, size=n_processos)
    
    # Tempo de tramitação (em dias)
    tempo_tramitacao = np.random.gamma(shape=2, scale=180, size=n_processos)
    
    # Resultado (0 = Improcedente, 1 = Procedente)
    # Influenciado por classe e juiz
    prob_procedente = 0.5 + 0.1 * (classes == 'Cível') - 0.1 * (classes == 'Criminal')
    resultado = np.random.binomial(1, prob_procedente)
    
    # Status (para análise de sobrevivência: 1 = encerrado, 0 = em andamento)
    status = np.random.binomial(1, 0.8, size=n_processos)
    
    # Tribunal (piloto)
    tribunais = np.random.choice(['TJ-SP', 'TJ-RJ', 'TJ-MG'], size=n_processos, p=[0.4, 0.35, 0.25])
    
    df = pd.DataFrame({
        'processo_id': [f'PROC-{i:05d}' for i in range(n_processos)],
        'tribunal': tribunais,
        'juiz': juizes,
        'classe': classes,
        'valor_causa': valores_causa,
        'tempo_tramitacao_dias': tempo_tramitacao,
        'resultado': resultado,
        'status': status,
        'data_distribuicao': pd.date_range(start='2020-01-01', periods=n_processos, freq='2D')
    })
    
    return df


def analise_descritiva(df, output_dir):
    """
    Realiza análise descritiva dos dados e gera visualizações.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com dados processuais
    output_dir : Path
        Diretório para salvar outputs
    """
    print("\n" + "="*60)
    print("ANÁLISE DESCRITIVA")
    print("="*60)
    
    # Estatísticas básicas
    print("\nEstatísticas Descritivas:")
    print(df[['valor_causa', 'tempo_tramitacao_dias']].describe())
    
    # Distribuição por classe
    print("\nDistribuição por Classe Processual:")
    print(df['classe'].value_counts())
    
    # Distribuição por tribunal
    print("\nDistribuição por Tribunal:")
    print(df['tribunal'].value_counts())
    
    # Taxa de procedência
    taxa_procedente = df['resultado'].mean() * 100
    print(f"\nTaxa de Procedência: {taxa_procedente:.2f}%")
    
    # Visualização 1: Distribuição do tempo de tramitação
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df['tempo_tramitacao_dias'], bins=30, edgecolor='black', alpha=0.7)
    ax.set_xlabel('Tempo de Tramitação (dias)', fontsize=12)
    ax.set_ylabel('Frequência', fontsize=12)
    ax.set_title('Distribuição do Tempo de Tramitação', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'distribuicao_tempo_tramitacao.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Visualização 2: Resultado por juiz
    fig, ax = plt.subplots(figsize=(10, 6))
    resultado_juiz = df.groupby(['juiz', 'resultado']).size().unstack(fill_value=0)
    resultado_juiz.plot(kind='bar', stacked=False, ax=ax, color=['#e74c3c', '#2ecc71'])
    ax.set_xlabel('Juiz', fontsize=12)
    ax.set_ylabel('Quantidade de Processos', fontsize=12)
    ax.set_title('Resultados por Juiz', fontsize=14, fontweight='bold')
    ax.legend(['Improcedente', 'Procedente'], loc='upper right')
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_dir / 'resultado_por_juiz.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Visualização 3: Boxplot do valor da causa por resultado
    fig, ax = plt.subplots(figsize=(10, 6))
    df_boxplot = df.copy()
    df_boxplot['resultado_label'] = df_boxplot['resultado'].map({0: 'Improcedente', 1: 'Procedente'})
    sns.boxplot(data=df_boxplot, x='resultado_label', y='valor_causa', ax=ax, palette='Set2')
    ax.set_xlabel('Resultado', fontsize=12)
    ax.set_ylabel('Valor da Causa (R$)', fontsize=12)
    ax.set_title('Distribuição do Valor da Causa por Resultado', fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    plt.tight_layout()
    plt.savefig(output_dir / 'boxplot_valor_causa.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ Visualizações salvas em {output_dir}")


def analise_preditiva(df, output_dir):
    """
    Realiza análise preditiva usando regressão logística.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com dados processuais
    output_dir : Path
        Diretório para salvar outputs
    """
    print("\n" + "="*60)
    print("ANÁLISE PREDITIVA - REGRESSÃO LOGÍSTICA")
    print("="*60)
    
    # Preparação dos dados
    df_model = df.copy()
    
    # Criar variáveis dummy
    df_model = pd.get_dummies(df_model, columns=['juiz', 'classe', 'tribunal'], drop_first=True)
    
    # Criar faixas de valor
    df_model['faixa_valor'] = pd.cut(
        df_model['valor_causa'],
        bins=[0, 10000, 50000, np.inf],
        labels=['Baixo', 'Médio', 'Alto']
    )
    df_model = pd.get_dummies(df_model, columns=['faixa_valor'], drop_first=True)
    
    # Selecionar features
    feature_cols = [col for col in df_model.columns if col.startswith(('juiz_', 'classe_', 'tribunal_', 'faixa_valor_', 'tempo_tramitacao'))]
    X = df_model[feature_cols]
    y = df_model['resultado']
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Treinar modelo
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    
    # Predições
    y_pred = model.predict(X_test)
    
    # Avaliação
    print("\nRelatório de Classificação (Conjunto de Teste):")
    report = classification_report(y_test, y_pred)
    print(report)
    
    # Salvar relatório
    with open(output_dir / 'classification_report.txt', 'w', encoding='utf-8') as f:
        f.write("Classification report (test)\n")
        f.write(report)
    
    # Matriz de confusão
    cm = confusion_matrix(y_test, y_pred)
    pd.DataFrame(cm).to_csv(output_dir / 'confusion_matrix.csv', index=False)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    print(f"\nAcurácia Cross-Validation (5-fold): {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
    
    # Salvar CV scores
    pd.DataFrame({'fold': range(1, 6), 'accuracy': cv_scores}).to_csv(
        output_dir / 'cv_scores.csv', index=False
    )
    
    # Odds Ratios
    odds_ratios = np.exp(model.coef_[0])
    feature_importance = pd.DataFrame({
        'Variável': X.columns,
        'Odds Ratio (Razão de Chances)': odds_ratios
    }).sort_values('Odds Ratio (Razão de Chances)', ascending=False)
    
    print("\nOdds Ratios das Variáveis:")
    print(feature_importance)
    
    feature_importance.to_csv(output_dir / 'resultados_regressao_logistica.csv', index=False)
    
    print(f"\n✓ Resultados da regressão logística salvos em {output_dir}")


def analise_sobrevivencia(df, output_dir):
    """
    Realiza análise de sobrevivência (tempo até encerramento do processo).
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com dados processuais
    output_dir : Path
        Diretório para salvar outputs
    """
    print("\n" + "="*60)
    print("ANÁLISE DE SOBREVIVÊNCIA")
    print("="*60)
    
    # Kaplan-Meier por classe processual
    fig, ax = plt.subplots(figsize=(12, 7))
    
    kmf = KaplanMeierFitter()
    
    for classe in df['classe'].unique():
        mask = df['classe'] == classe
        kmf.fit(
            df.loc[mask, 'tempo_tramitacao_dias'],
            df.loc[mask, 'status'],
            label=classe
        )
        kmf.plot_survival_function(ax=ax, ci_show=True)
    
    ax.set_xlabel('Tempo (dias)', fontsize=12)
    ax.set_ylabel('Probabilidade de Sobrevivência (Processo ainda em andamento)', fontsize=12)
    ax.set_title('Curva de Sobrevivência Kaplan-Meier por Classe Processual', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'kaplan_meier_survival.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Teste Log-Rank
    try:
        results = multivariate_logrank_test(
            df['tempo_tramitacao_dias'],
            df['classe'],
            df['status']
        )
        print(f"\nTeste Log-Rank (comparação entre classes):")
        print(f"  Estatística: {results.test_statistic:.4f}")
        print(f"  p-valor: {results.p_value:.4f}")
        
        if results.p_value < 0.05:
            print("  → Diferença SIGNIFICATIVA entre as curvas de sobrevivência")
        else:
            print("  → Diferença NÃO significativa entre as curvas de sobrevivência")
    except Exception as e:
        print(f"Aviso: Não foi possível executar teste Log-Rank: {e}")
    
    # Modelo Cox de Riscos Proporcionais
    print("\nModelo de Cox (Riscos Proporcionais):")
    
    df_cox = df.copy()
    df_cox = pd.get_dummies(df_cox, columns=['juiz', 'classe', 'tribunal'], drop_first=True)
    
    cph_cols = ['tempo_tramitacao_dias', 'status'] + [col for col in df_cox.columns if col.startswith(('juiz_', 'classe_', 'tribunal_'))]
    df_cox_model = df_cox[cph_cols].copy()
    
    cph = CoxPHFitter()
    try:
        cph.fit(df_cox_model, duration_col='tempo_tramitacao_dias', event_col='status')
        
        print("\nSumário do Modelo Cox:")
        print(cph.summary[['coef', 'exp(coef)', 'p']])
        
        # Salvar hazard ratios
        hazard_summary = cph.summary[['coef', 'exp(coef)', 'p']].copy()
        hazard_summary.columns = ['Coeficiente', 'Hazard Ratio', 'p-valor']
        hazard_summary.to_csv(output_dir / 'hazard_ratios_cox.csv')
        
    except Exception as e:
        print(f"Aviso: Não foi possível ajustar modelo Cox: {e}")
        # Criar arquivo vazio para manter consistência
        pd.DataFrame({
            'Variável': ['N/A'],
            'Coeficiente': [0],
            'Hazard Ratio': [1],
            'p-valor': [1]
        }).to_csv(output_dir / 'hazard_ratios_cox.csv', index=False)
    
    print(f"\n✓ Análise de sobrevivência completa. Gráficos salvos em {output_dir}")


def analise_quebra_estrutural(df, output_dir):
    """
    Simula detecção de quebra estrutural na série temporal de processos.
    
    Em produção, usaríamos métodos como CUSUM ou Chow test.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com dados processuais
    output_dir : Path
        Diretório para salvar outputs
    """
    print("\n" + "="*60)
    print("ANÁLISE DE QUEBRA ESTRUTURAL")
    print("="*60)
    
    # Agregar por data
    df_temporal = df.copy()
    df_temporal['mes'] = df_temporal['data_distribuicao'].dt.to_period('M')
    serie_mensal = df_temporal.groupby('mes').size()
    
    # Simular quebra (para demonstração)
    ponto_quebra = len(serie_mensal) // 2
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(range(len(serie_mensal)), serie_mensal.values, 'o-', label='Processos por mês', linewidth=2)
    ax.axvline(x=ponto_quebra, color='red', linestyle='--', linewidth=2, label=f'Quebra Estrutural (simulada)')
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Número de Processos Distribuídos', fontsize=12)
    ax.set_title('Detecção de Quebra Estrutural na Série Temporal', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'quebra_estrutural_detectada.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Quebra estrutural detectada no mês {ponto_quebra} (simulação)")
    print(f"  Visualização salva em {output_dir}")


def gerar_relatorio_json(df, output_dir):
    """
    Gera um relatório em formato JSON com estatísticas principais.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com dados processuais
    output_dir : Path
        Diretório para salvar output
    """
    relatorio = {
        'metadata': {
            'data_geracao': datetime.now().isoformat(),
            'versao_script': '1.0.0',
            'n_processos': len(df)
        },
        'estatisticas': {
            'tempo_tramitacao': {
                'media_dias': float(df['tempo_tramitacao_dias'].mean()),
                'mediana_dias': float(df['tempo_tramitacao_dias'].median()),
                'desvio_padrao_dias': float(df['tempo_tramitacao_dias'].std()),
                'minimo_dias': float(df['tempo_tramitacao_dias'].min()),
                'maximo_dias': float(df['tempo_tramitacao_dias'].max())
            },
            'valor_causa': {
                'media_reais': float(df['valor_causa'].mean()),
                'mediana_reais': float(df['valor_causa'].median()),
                'desvio_padrao_reais': float(df['valor_causa'].std())
            },
            'resultados': {
                'taxa_procedencia_pct': float(df['resultado'].mean() * 100),
                'total_procedentes': int(df['resultado'].sum()),
                'total_improcedentes': int((df['resultado'] == 0).sum())
            },
            'distribuicao_classe': df['classe'].value_counts().to_dict(),
            'distribuicao_tribunal': df['tribunal'].value_counts().to_dict(),
            'distribuicao_juiz': df['juiz'].value_counts().to_dict()
        }
    }
    
    with open(output_dir / 'relatorio_estatisticas.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Relatório JSON salvo em {output_dir / 'relatorio_estatisticas.json'}")


def main():
    """
    Função principal que executa todo o pipeline de análise.
    """
    print("\n" + "="*60)
    print("ANÁLISE JURIMÉTRICA COMPLETA")
    print("="*60)
    print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Gerar ou carregar dados
    print("\n[1/6] Gerando/Carregando dados...")
    df = gerar_dados_simulados(n_processos=150)
    
    # Salvar dados simulados
    DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(DATA_DIR / 'dados_simulados.csv', index=False, encoding='utf-8')
    print(f"  ✓ Dados salvos em {DATA_DIR / 'dados_simulados.csv'}")
    
    # Análises
    print("\n[2/6] Executando análise descritiva...")
    analise_descritiva(df, OUTPUT_DIR)
    
    print("\n[3/6] Executando análise preditiva...")
    analise_preditiva(df, OUTPUT_DIR)
    
    print("\n[4/6] Executando análise de sobrevivência...")
    analise_sobrevivencia(df, OUTPUT_DIR)
    
    print("\n[5/6] Executando análise de quebra estrutural...")
    analise_quebra_estrutural(df, OUTPUT_DIR)
    
    print("\n[6/6] Gerando relatório JSON...")
    gerar_relatorio_json(df, OUTPUT_DIR)
    
    # Gerar relatório HTML
    print("\nGerando relatório HTML completo...")
    try:
        import subprocess
        subprocess.run(['python3', str(BASE_DIR / 'generate_report_complete.py')], check=True)
    except Exception as e:
        print(f"Aviso: Não foi possível gerar relatório HTML: {e}")
    
    print("\n" + "="*60)
    print("ANÁLISE COMPLETA!")
    print("="*60)
    print(f"Fim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nTodos os resultados foram salvos em: {OUTPUT_DIR}")
    print("\nArquivos gerados:")
    for file in sorted(OUTPUT_DIR.glob('*')):
        print(f"  - {file.name}")


if __name__ == '__main__':
    main()
