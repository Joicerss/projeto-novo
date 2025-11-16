#!/usr/bin/env python3
"""
Pipeline para consolidar CSVs e gerar flags para processos de recuperação judicial.

Este script consolida múltiplos arquivos CSV de processos judiciais e gera flags
(sinalizadores) baseados em heurísticas para responder às 14 questões sobre
recuperação judicial.

Entrada: Arquivos CSV na pasta 'data/' com informações de processos
Saída: 
  - outputs/consolidado_flags.csv
  - outputs/consolidado_flags.json
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import re


def normalize_process_number(num_str):
    """
    Normaliza o número do processo removendo caracteres especiais.
    
    Args:
        num_str: String com número do processo
        
    Returns:
        String normalizada contendo apenas dígitos
    """
    if pd.isna(num_str):
        return ""
    return re.sub(r'\D', '', str(num_str))


def identify_flags(row):
    """
    Identifica flags baseadas em heurísticas sobre o processo.
    
    Args:
        row: Linha do DataFrame com informações do processo
        
    Returns:
        Dict com flags identificadas
    """
    flags = {
        'tem_recurso': False,
        'tem_agravo': False,
        'tem_apelacao': False,
        'tem_embargos': False,
        'tem_liminar': False,
        'tem_decisao_monocrática': False,
        'tem_sentenca': False,
        'tem_acordao': False,
        'processo_ativo': False,
        'processo_arquivado': False,
        'processo_suspenso': False,
        'valor_causa_alto': False,
        'valor_causa_baixo': False,
        'tempo_tramitacao_longo': False,
    }
    
    # Análise do assunto/classe do processo
    assunto = str(row.get('assunto', '')).lower()
    classe = str(row.get('classe', '')).lower()
    movimentacoes = str(row.get('movimentacoes', '')).lower()
    
    # Identificar tipos de recursos
    if 'recurso' in assunto or 'recurso' in classe or 'recurso' in movimentacoes:
        flags['tem_recurso'] = True
    
    if 'agravo' in assunto or 'agravo' in classe or 'agravo' in movimentacoes:
        flags['tem_agravo'] = True
    
    if 'apelação' in assunto or 'apelação' in classe or 'apelacao' in movimentacoes:
        flags['tem_apelacao'] = True
    
    if 'embargo' in assunto or 'embargo' in classe or 'embargo' in movimentacoes:
        flags['tem_embargos'] = True
    
    # Identificar decisões
    if 'liminar' in movimentacoes:
        flags['tem_liminar'] = True
    
    if 'decisão monocrática' in movimentacoes or 'decisao monocratica' in movimentacoes:
        flags['tem_decisao_monocrática'] = True
    
    if 'sentença' in movimentacoes or 'sentenca' in movimentacoes:
        flags['tem_sentenca'] = True
    
    if 'acórdão' in movimentacoes or 'acordao' in movimentacoes:
        flags['tem_acordao'] = True
    
    # Análise do status
    situacao = str(row.get('situacao', '')).lower()
    
    if 'ativo' in situacao or 'andamento' in situacao:
        flags['processo_ativo'] = True
    
    if 'arquivado' in situacao or 'baixado' in situacao:
        flags['processo_arquivado'] = True
    
    if 'suspenso' in situacao or 'sobrestado' in situacao:
        flags['processo_suspenso'] = True
    
    # Análise do valor da causa
    valor_causa = row.get('valor_causa', 0)
    if pd.notna(valor_causa):
        try:
            valor = float(valor_causa)
            if valor > 1000000:  # Mais de 1 milhão
                flags['valor_causa_alto'] = True
            elif valor < 100000:  # Menos de 100 mil
                flags['valor_causa_baixo'] = True
        except (ValueError, TypeError):
            pass
    
    # Análise do tempo de tramitação
    data_distribuicao = row.get('data_distribuicao')
    if pd.notna(data_distribuicao):
        try:
            data_dist = pd.to_datetime(data_distribuicao, errors='coerce')
            if pd.notna(data_dist):
                dias_tramitacao = (datetime.now() - data_dist).days
                if dias_tramitacao > 730:  # Mais de 2 anos
                    flags['tempo_tramitacao_longo'] = True
        except Exception:
            pass
    
    return flags


def load_and_consolidate_csvs(data_dir):
    """
    Carrega e consolida todos os CSVs da pasta data/.
    
    Args:
        data_dir: Path para o diretório com os CSVs
        
    Returns:
        DataFrame consolidado
    """
    csv_files = list(data_dir.glob('*.csv'))
    
    if not csv_files:
        print(f"⚠️  Nenhum arquivo CSV encontrado em {data_dir}")
        print("Criando dataset de exemplo...")
        # Criar um dataset de exemplo para demonstração
        df_exemplo = pd.DataFrame({
            'numero_processo': ['0001234-56.2023.8.26.0100', '0009876-54.2023.8.26.0200'],
            'classe': ['Recuperação Judicial', 'Recuperação Judicial'],
            'assunto': ['Recuperação Judicial', 'Plano de Recuperação'],
            'data_distribuicao': ['2023-01-15', '2023-03-20'],
            'valor_causa': [5000000.00, 850000.00],
            'situacao': ['Em andamento', 'Ativo'],
            'movimentacoes': ['Distribuição; Liminar deferida; Sentença proferida', 'Distribuição; Decisão monocrática'],
        })
        return df_exemplo
    
    print(f"📂 Carregando {len(csv_files)} arquivo(s) CSV...")
    
    dataframes = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            print(f"  ✓ {csv_file.name}: {len(df)} linhas")
            dataframes.append(df)
        except Exception as e:
            print(f"  ✗ Erro ao carregar {csv_file.name}: {e}")
    
    if not dataframes:
        raise ValueError("Nenhum CSV pôde ser carregado com sucesso")
    
    # Consolidar todos os DataFrames
    df_consolidated = pd.concat(dataframes, ignore_index=True)
    print(f"\n📊 Total de processos consolidados: {len(df_consolidated)}")
    
    return df_consolidated


def main():
    """Função principal do pipeline."""
    print("=" * 60)
    print("Pipeline: Consolidação de CSVs e Geração de Flags")
    print("=" * 60)
    print()
    
    # Definir diretórios
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    output_dir = base_dir / 'outputs'
    
    # Criar diretório de saída se não existir
    output_dir.mkdir(exist_ok=True)
    
    # Carregar e consolidar CSVs
    df = load_and_consolidate_csvs(data_dir)
    
    # Normalizar números de processo
    if 'numero_processo' in df.columns:
        print("\n🔄 Normalizando números de processo...")
        df['numero_processo_normalizado'] = df['numero_processo'].apply(normalize_process_number)
    
    # Gerar flags para cada processo
    print("\n🏁 Gerando flags para cada processo...")
    flags_list = []
    for idx, row in df.iterrows():
        flags = identify_flags(row)
        flags_list.append(flags)
    
    # Adicionar flags ao DataFrame
    flags_df = pd.DataFrame(flags_list)
    df_with_flags = pd.concat([df, flags_df], axis=1)
    
    # Salvar resultados
    output_csv = output_dir / 'consolidado_flags.csv'
    output_json = output_dir / 'consolidado_flags.json'
    
    print(f"\n💾 Salvando resultados...")
    df_with_flags.to_csv(output_csv, index=False)
    print(f"  ✓ CSV salvo em: {output_csv}")
    
    # Salvar também em JSON para facilitar leitura
    df_with_flags.to_json(output_json, orient='records', indent=2, force_ascii=False)
    print(f"  ✓ JSON salvo em: {output_json}")
    
    # Resumo estatístico
    print("\n" + "=" * 60)
    print("📈 Resumo Estatístico das Flags")
    print("=" * 60)
    
    for col in flags_df.columns:
        count = flags_df[col].sum()
        percentage = (count / len(flags_df)) * 100
        print(f"  {col:30s}: {count:4d} ({percentage:5.1f}%)")
    
    print("\n✅ Pipeline concluído com sucesso!")
    print(f"\n💡 Próximo passo: Visualize os resultados em {output_csv}")
    print("   ou execute o notebook Jupyter para análise interativa.")
    

if __name__ == '__main__':
    main()
