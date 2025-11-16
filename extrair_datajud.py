"""
Script principal para extração de dados do DataJud/CNJ
Autor: Projeto Jurimetria
Data: 2025-11-16
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv
import pandas as pd
from tqdm import tqdm

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/extracao.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()


class DataJudExtractor:
    """Classe para extração de dados do DataJud/CNJ"""
    
    def __init__(self, api_key: Optional[str] = None, use_proxy: bool = False):
        """
        Inicializa o extrator DataJud
        
        Args:
            api_key: Chave de API do DataJud (ou carrega de .env)
            use_proxy: Se deve usar proxy para as requisições
        """
        self.api_key = api_key or os.getenv('DATAJUD_API_KEY', '')
        self.base_url = os.getenv('DATAJUD_BASE_URL', 'https://api-publica.datajud.cnj.jus.br')
        self.use_proxy = use_proxy
        self.session = self._criar_sessao()
        
        # Criar diretórios necessários
        Path('dados').mkdir(exist_ok=True)
        Path('resultados').mkdir(exist_ok=True)
        Path('logs').mkdir(exist_ok=True)
        
    def _criar_sessao(self) -> requests.Session:
        """Cria sessão HTTP com configurações apropriadas"""
        session = requests.Session()
        
        if self.api_key:
            session.headers.update({
                'Authorization': f'APIKey {self.api_key}',
                'Content-Type': 'application/json'
            })
        
        if self.use_proxy:
            proxy_url = os.getenv('PROXY_URL', '')
            if proxy_url:
                session.proxies = {
                    'http': proxy_url,
                    'https': proxy_url
                }
        
        return session
    
    def buscar_processo(self, numero_processo: str) -> Optional[Dict]:
        """
        Busca dados de um processo específico
        
        Args:
            numero_processo: Número do processo (formato CNJ)
        
        Returns:
            Dicionário com dados do processo ou None em caso de erro
        """
        try:
            logger.info(f"Buscando processo: {numero_processo}")
            
            # Endpoint de exemplo - ajustar conforme API real do DataJud
            url = f"{self.base_url}/api_publica_processos/_search"
            
            payload = {
                "query": {
                    "match": {
                        "numeroProcesso": numero_processo
                    }
                }
            }
            
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Processo {numero_processo} encontrado")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar processo {numero_processo}: {e}")
            return None
    
    def extrair_campos_cnj(self, dados_processo: Dict) -> Dict:
        """
        Extrai os 14 campos principais conforme padrão CNJ
        
        Args:
            dados_processo: Dados brutos do processo
        
        Returns:
            Dicionário com os 14 campos extraídos
        """
        campos = {
            '1_numero_processo': '',
            '2_classe': '',
            '3_assunto': '',
            '4_data_ajuizamento': '',
            '5_orgao_julgador': '',
            '6_magistrado': '',
            '7_valor_causa': '',
            '8_partes_polo_ativo': '',
            '9_partes_polo_passivo': '',
            '10_movimentacoes': [],
            '11_data_ultima_movimentacao': '',
            '12_situacao_processo': '',
            '13_data_transito_julgado': '',
            '14_resultado': ''
        }
        
        try:
            # Extração de exemplo - ajustar conforme estrutura real
            hits = dados_processo.get('hits', {}).get('hits', [])
            
            if hits:
                processo = hits[0].get('_source', {})
                
                campos['1_numero_processo'] = processo.get('numeroProcesso', '')
                campos['2_classe'] = processo.get('classe', {}).get('nome', '')
                campos['3_assunto'] = processo.get('assunto', {}).get('nome', '')
                campos['4_data_ajuizamento'] = processo.get('dataAjuizamento', '')
                campos['5_orgao_julgador'] = processo.get('orgaoJulgador', {}).get('nome', '')
                campos['6_magistrado'] = processo.get('magistrado', {}).get('nome', '')
                campos['7_valor_causa'] = processo.get('valorCausa', '')
                
                # Partes
                partes_ativas = []
                partes_passivas = []
                
                for parte in processo.get('partes', []):
                    nome = parte.get('nome', '')
                    polo = parte.get('polo', '')
                    
                    if polo.upper() == 'ATIVO':
                        partes_ativas.append(nome)
                    elif polo.upper() == 'PASSIVO':
                        partes_passivas.append(nome)
                
                campos['8_partes_polo_ativo'] = '; '.join(partes_ativas)
                campos['9_partes_polo_passivo'] = '; '.join(partes_passivas)
                
                # Movimentações
                movimentacoes = processo.get('movimentos', [])
                campos['10_movimentacoes'] = movimentacoes
                
                if movimentacoes:
                    campos['11_data_ultima_movimentacao'] = movimentacoes[-1].get('dataHora', '')
                
                campos['12_situacao_processo'] = processo.get('situacao', '')
                campos['13_data_transito_julgado'] = processo.get('dataTransitoJulgado', '')
                campos['14_resultado'] = processo.get('resultado', '')
        
        except Exception as e:
            logger.error(f"Erro ao extrair campos: {e}")
        
        return campos
    
    def processar_lote(self, numeros_processos: List[str]) -> pd.DataFrame:
        """
        Processa um lote de processos
        
        Args:
            numeros_processos: Lista de números de processos
        
        Returns:
            DataFrame com dados extraídos
        """
        resultados = []
        
        for numero in tqdm(numeros_processos, desc="Processando"):
            dados = self.buscar_processo(numero)
            
            if dados:
                campos = self.extrair_campos_cnj(dados)
                resultados.append(campos)
            else:
                # Registrar processo não encontrado
                resultados.append({
                    '1_numero_processo': numero,
                    'erro': 'Processo não encontrado'
                })
        
        df = pd.DataFrame(resultados)
        
        # Salvar resultados
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'resultados/extracao_{timestamp}.xlsx'
        df.to_excel(output_file, index=False)
        logger.info(f"Resultados salvos em: {output_file}")
        
        return df
    
    def validar_cnj(self, numero_processo: str) -> bool:
        """
        Valida se o número do processo está no formato CNJ correto
        
        Args:
            numero_processo: Número do processo
        
        Returns:
            True se válido, False caso contrário
        """
        # Formato CNJ: NNNNNNN-DD.AAAA.J.TR.OOOO
        # 7 dígitos - 2 dígitos verificadores . 4 dígitos ano . 1 segmento . 2 tribunal . 4 origem
        
        import re
        
        # Remove espaços e hífens extras
        numero = numero_processo.replace(' ', '').replace('-', '')
        
        # Padrão: 7 dígitos, 2 dígitos, 4 dígitos, 1 dígito, 2 dígitos, 4 dígitos
        padrao = r'^\d{7}\d{2}\d{4}\d{1}\d{2}\d{4}$'
        
        if not re.match(padrao, numero):
            return False
        
        # Validação do dígito verificador (algoritmo CNJ)
        # Implementação simplificada - pode ser expandida
        return True


def main():
    """Função principal"""
    logger.info("Iniciando extração DataJud")
    
    # Criar extrator
    extractor = DataJudExtractor()
    
    # Processos de exemplo (5 processos para teste)
    processos_exemplo = [
        '0000001-01.2024.8.00.0001',
        '0000002-01.2024.8.00.0001',
        '0000003-01.2024.8.00.0001',
        '0000004-01.2024.8.00.0001',
        '0000005-01.2024.8.00.0001'
    ]
    
    # Validar números
    for num in processos_exemplo:
        if extractor.validar_cnj(num):
            logger.info(f"Número válido: {num}")
        else:
            logger.warning(f"Número inválido: {num}")
    
    # Processar lote
    # NOTA: Descomente a linha abaixo para executar extração real
    # df_resultados = extractor.processar_lote(processos_exemplo)
    
    logger.info("Extração concluída")


if __name__ == '__main__':
    main()
