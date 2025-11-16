# Guia de Integração com DataJud

## Visão Geral

Este guia explica como integrar o projeto com a API do DataJud (CNJ) para coletar dados judiciais reais.

## Pré-requisitos

1. **Credenciais de API**: Obtenha credenciais de acesso à API do DataJud através do CNJ
2. **Conformidade LGPD**: Certifique-se de que seu uso está em conformidade com a Lei Geral de Proteção de Dados
3. **Autorização Institucional**: Obtenha as autorizações necessárias da sua instituição

## Configuração

### 1. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# API DataJud/CNJ
DATAJUD_API_URL=https://api.datajud.cnj.jus.br
DATAJUD_API_KEY=sua-chave-api-aqui
DATAJUD_CLIENT_ID=seu-client-id
DATAJUD_CLIENT_SECRET=seu-client-secret

# Configurações de coleta
DATAJUD_TIMEOUT=30
DATAJUD_MAX_RETRIES=3
DATAJUD_RATE_LIMIT=100  # requisições por minuto
```

### 2. Instalar Dependências Adicionais

```bash
pip install requests python-dotenv pyjwt
```

## Estrutura de Dados do DataJud

A API do DataJud retorna dados no formato JSON com a seguinte estrutura (simplificada):

```json
{
  "processo": {
    "numero": "0001234-56.2023.8.26.0100",
    "tribunal": "TJSP",
    "classe": {
      "codigo": "1",
      "nome": "Procedimento Comum Cível"
    },
    "assunto": {
      "codigo": "1234",
      "nome": "Dano Material"
    },
    "valorCausa": 50000.00,
    "dataAjuizamento": "2023-01-15",
    "orgaoJulgador": {
      "codigo": "001",
      "nome": "1ª Vara Cível"
    },
    "magistrado": "Nome do Juiz",
    "movimentacoes": [
      {
        "data": "2023-01-15",
        "codigo": "123",
        "nome": "Distribuído por sorteio"
      }
    ]
  }
}
```

## Implementação

### Script de Coleta

Crie um arquivo `coleta_datajud.py`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Coleta de Dados do DataJud
====================================

Coleta dados judiciais da API do DataJud/CNJ.
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()


class DataJudCollector:
    """Classe para coleta de dados do DataJud."""
    
    def __init__(self):
        """Inicializa o coletor."""
        self.api_url = os.getenv('DATAJUD_API_URL')
        self.api_key = os.getenv('DATAJUD_API_KEY')
        self.client_id = os.getenv('DATAJUD_CLIENT_ID')
        self.client_secret = os.getenv('DATAJUD_CLIENT_SECRET')
        self.timeout = int(os.getenv('DATAJUD_TIMEOUT', 30))
        self.max_retries = int(os.getenv('DATAJUD_MAX_RETRIES', 3))
        self.rate_limit = int(os.getenv('DATAJUD_RATE_LIMIT', 100))
        
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
        
        self.last_request_time = None
        
    def _rate_limit_wait(self):
        """Implementa rate limiting."""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            min_interval = 60 / self.rate_limit
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """
        Faz requisição à API com retry.
        
        Parameters
        ----------
        endpoint : str
            Endpoint da API
        params : Dict
            Parâmetros da requisição
            
        Returns
        -------
        Optional[Dict]
            Resposta da API ou None em caso de erro
        """
        self._rate_limit_wait()
        
        url = f"{self.api_url}/{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Tentativa {attempt + 1} falhou: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Falha após {self.max_retries} tentativas")
                    return None
    
    def coletar_processos(
        self,
        tribunal: str,
        data_inicio: str,
        data_fim: str,
        classe: Optional[str] = None
    ) -> List[Dict]:
        """
        Coleta processos do DataJud.
        
        Parameters
        ----------
        tribunal : str
            Sigla do tribunal (ex: 'TJSP', 'TJRJ')
        data_inicio : str
            Data inicial (formato: YYYY-MM-DD)
        data_fim : str
            Data final (formato: YYYY-MM-DD)
        classe : Optional[str]
            Código da classe processual (opcional)
            
        Returns
        -------
        List[Dict]
            Lista de processos
        """
        logger.info(f"Coletando processos de {tribunal} entre {data_inicio} e {data_fim}")
        
        params = {
            'tribunal': tribunal,
            'dataInicio': data_inicio,
            'dataFim': data_fim,
            'limite': 100  # processos por página
        }
        
        if classe:
            params['classe'] = classe
        
        processos = []
        pagina = 1
        
        while True:
            params['pagina'] = pagina
            
            response = self._make_request('processos', params)
            if not response or 'dados' not in response:
                break
            
            processos.extend(response['dados'])
            
            # Verificar se há mais páginas
            if len(response['dados']) < params['limite']:
                break
            
            pagina += 1
            logger.info(f"Coletados {len(processos)} processos até agora...")
        
        logger.info(f"Coleta finalizada: {len(processos)} processos")
        return processos
    
    def transformar_para_dataframe(self, processos: List[Dict]) -> pd.DataFrame:
        """
        Transforma dados coletados em DataFrame padronizado.
        
        Parameters
        ----------
        processos : List[Dict]
            Lista de processos do DataJud
            
        Returns
        -------
        pd.DataFrame
            DataFrame padronizado
        """
        dados_transformados = []
        
        for processo in processos:
            # Calcular tempo de tramitação
            data_inicio = pd.to_datetime(processo.get('dataAjuizamento'))
            
            # Se processo encerrado, usar data de encerramento
            # Senão, usar data atual
            movimentacoes = processo.get('movimentacoes', [])
            data_fim = None
            status = 0  # Em andamento
            
            for mov in movimentacoes:
                if 'encerr' in mov.get('nome', '').lower() or 'arquiv' in mov.get('nome', '').lower():
                    data_fim = pd.to_datetime(mov['data'])
                    status = 1  # Encerrado
                    break
            
            if not data_fim:
                data_fim = pd.Timestamp.now()
            
            tempo_tramitacao = (data_fim - data_inicio).days
            
            # Determinar resultado (exemplo simplificado)
            resultado = 0  # Padrão: improcedente
            for mov in movimentacoes:
                nome_mov = mov.get('nome', '').lower()
                if 'proced' in nome_mov or 'julg' in nome_mov and 'favor' in nome_mov:
                    resultado = 1
                    break
            
            dados_transformados.append({
                'processo_id': processo.get('numero'),
                'tribunal': processo.get('tribunal'),
                'juiz': processo.get('magistrado', 'N/A'),
                'classe': processo.get('classe', {}).get('nome', 'N/A'),
                'valor_causa': float(processo.get('valorCausa', 0)),
                'tempo_tramitacao_dias': tempo_tramitacao,
                'resultado': resultado,
                'status': status,
                'data_distribuicao': data_inicio,
                'assunto': processo.get('assunto', {}).get('nome', 'N/A')
            })
        
        return pd.DataFrame(dados_transformados)


def main():
    """Função principal."""
    # Inicializar coletor
    collector = DataJudCollector()
    
    # Definir parâmetros de coleta
    # Exemplo: coletar processos dos últimos 6 meses
    data_fim = datetime.now()
    data_inicio = data_fim - timedelta(days=180)
    
    tribunais = ['TJSP', 'TJRJ', 'TJMG']  # Tribunais pilotos
    
    todos_processos = []
    
    for tribunal in tribunais:
        logger.info(f"\n{'='*60}")
        logger.info(f"Coletando dados de {tribunal}")
        logger.info(f"{'='*60}")
        
        processos = collector.coletar_processos(
            tribunal=tribunal,
            data_inicio=data_inicio.strftime('%Y-%m-%d'),
            data_fim=data_fim.strftime('%Y-%m-%d')
        )
        
        todos_processos.extend(processos)
    
    # Transformar para DataFrame
    logger.info("\nTransformando dados...")
    df = collector.transformar_para_dataframe(todos_processos)
    
    # Salvar dados
    output_dir = Path(__file__).parent / 'data'
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f'dados_datajud_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    logger.info(f"\n✓ Dados salvos em: {output_file}")
    logger.info(f"Total de processos coletados: {len(df)}")
    
    # Mostrar estatísticas básicas
    logger.info("\nEstatísticas básicas:")
    logger.info(df.describe())


if __name__ == '__main__':
    main()
```

## Uso

### 1. Configurar Credenciais

Edite o arquivo `.env` com suas credenciais.

### 2. Executar Coleta

```bash
python coleta_datajud.py
```

### 3. Usar Dados Coletados

Modifique `jurimetria_completa.py` para carregar os dados coletados:

```python
# Em vez de gerar dados simulados
df = gerar_dados_simulados(n_processos=150)

# Use:
df = pd.read_csv('data/dados_datajud_YYYYMMDD_HHMMSS.csv')
```

## Limitações e Considerações

### Rate Limiting

A API do DataJud tem limites de requisições. O script implementa:
- Rate limiting automático
- Retry com exponential backoff
- Controle de requisições por minuto

### Conformidade LGPD

⚠️ **IMPORTANTE**: Ao trabalhar com dados reais:

1. **Anonimização**: Remova ou anonimize dados sensíveis (nomes de partes, CPFs, etc.)
2. **Finalidade**: Use dados apenas para fins estatísticos e pesquisa
3. **Armazenamento**: Armazene dados de forma segura
4. **Retenção**: Estabeleça política de retenção de dados
5. **Consentimento**: Verifique necessidade de consentimento para uso específico

### Exemplo de Anonimização

```python
def anonimizar_dados(df):
    """Anonimiza dados sensíveis."""
    df = df.copy()
    
    # Remover CPFs/CNPJs
    if 'cpf' in df.columns:
        df.drop('cpf', axis=1, inplace=True)
    
    # Hash de nomes de partes
    if 'parte_nome' in df.columns:
        df['parte_nome'] = df['parte_nome'].apply(
            lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:10]
        )
    
    # Generalizar juízes
    if 'juiz' in df.columns:
        df['juiz'] = df['juiz'].apply(lambda x: f"Juiz {hash(x) % 26 + 1}")
    
    return df
```

## Troubleshooting

### Erro de Autenticação

```
Erro 401: Unauthorized
```

**Solução**: Verifique suas credenciais no arquivo `.env`

### Rate Limit Exceeded

```
Erro 429: Too Many Requests
```

**Solução**: Ajuste `DATAJUD_RATE_LIMIT` no `.env` para um valor menor

### Timeout

```
Erro: Connection timeout
```

**Solução**: Aumente `DATAJUD_TIMEOUT` no `.env`

## Recursos Adicionais

- [Documentação oficial DataJud](https://www.cnj.jus.br/datajud)
- [Portal CNJ](https://www.cnj.jus.br)
- [Guia LGPD para pesquisadores](https://www.gov.br/lgpd)

## Suporte

Para questões sobre integração com DataJud:
- Abra uma issue no repositório
- Consulte a documentação oficial do CNJ
- Entre em contato com o suporte técnico do DataJud

---

**Nota**: Este guia é baseado em uma estrutura genérica de API. Adapte conforme a implementação real da API do DataJud/CNJ.
