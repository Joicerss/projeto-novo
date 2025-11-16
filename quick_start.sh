#!/bin/bash
# Script de Início Rápido para Projeto Jurimetria
# ================================================

set -e  # Sair em caso de erro

echo "=========================================="
echo "  Projeto Jurimetria - Início Rápido"
echo "=========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python encontrado:${NC} $(python3 --version)"
echo ""

# Verificar se está em ambiente virtual (recomendado)
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${YELLOW}⚠️  Aviso: Não está em um ambiente virtual.${NC}"
    echo "   Recomendamos criar um ambiente virtual:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate  # Linux/Mac"
    echo "   venv\\Scripts\\activate     # Windows"
    echo ""
    read -p "Deseja continuar mesmo assim? (s/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 0
    fi
fi

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependências instaladas com sucesso${NC}"
else
    echo -e "${RED}❌ Erro ao instalar dependências${NC}"
    exit 1
fi
echo ""

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p data output notebooks

# Gerar template Excel
echo "📊 Gerando planilha modelo..."
python3 criar_template.py

# Executar análise completa
echo ""
echo "🚀 Executando análise completa..."
echo "   (Isso pode levar alguns minutos)"
echo ""
python3 jurimetria_completa.py

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}=========================================="
    echo "  ✅ Análise Concluída com Sucesso!"
    echo "==========================================${NC}"
    echo ""
    echo "📂 Resultados salvos em:"
    echo "   - output/         (gráficos e tabelas)"
    echo "   - data/           (dados simulados)"
    echo ""
    echo "📄 Arquivos gerados:"
    ls -lh output/ | tail -n +2 | awk '{print "   -", $9, "(" $5 ")"}'
    echo ""
    echo "🔍 Próximos passos:"
    echo "   1. Visualize o relatório HTML: output/report_complete.html"
    echo "   2. Explore os dados no Jupyter: jupyter notebook notebooks/exemplo_workflow.ipynb"
    echo "   3. Execute validação: python3 validacao_dados.py"
    echo "   4. Execute testes: pytest test_jurimetria.py -v"
    echo ""
    echo "📚 Para mais informações, consulte o README.md"
else
    echo -e "${RED}❌ Erro ao executar análise${NC}"
    exit 1
fi
