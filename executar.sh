#!/bin/bash
# Script de execução do pacote DataJud/CNJ

echo "========================================"
echo "Pacote de Extração DataJud/CNJ"
echo "========================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.11 ou superior."
    exit 1
fi

echo "✓ Python encontrado: $(python3 --version)"

# Verificar ambiente virtual
if [ ! -d "venv" ]; then
    echo ""
    echo "Criando ambiente virtual..."
    python3 -m venv venv
    echo "✓ Ambiente virtual criado"
fi

# Ativar ambiente virtual
echo ""
echo "Ativando ambiente virtual..."
source venv/bin/activate
echo "✓ Ambiente virtual ativado"

# Instalar dependências
echo ""
echo "Instalando dependências..."
pip install -q -r requirements.txt
echo "✓ Dependências instaladas"

# Criar diretórios necessários
echo ""
echo "Criando diretórios..."
mkdir -p dados resultados logs
echo "✓ Diretórios criados"

# Verificar arquivo .env
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  Arquivo .env não encontrado!"
    echo "Copiando .env.exemplo para .env..."
    cp .env.exemplo .env
    echo "✓ Arquivo .env criado"
    echo ""
    echo "ATENÇÃO: Configure suas credenciais no arquivo .env antes de continuar!"
    echo "Edite o arquivo .env e adicione sua chave API do DataJud."
    echo ""
    read -p "Pressione ENTER para continuar (após configurar o .env)..."
fi

# Menu
echo ""
echo "Escolha uma opção:"
echo ""
echo "1. Executar validação CNJ (teste)"
echo "2. Executar extração DataJud"
echo "3. Abrir Jupyter Notebook"
echo "4. Executar todos os testes"
echo "5. Sair"
echo ""
read -p "Opção: " opcao

case $opcao in
    1)
        echo ""
        echo "Executando validação CNJ..."
        python3 validacao_cnj.py
        ;;
    2)
        echo ""
        echo "Executando extração DataJud..."
        python3 extrair_datajud.py
        ;;
    3)
        echo ""
        echo "Iniciando Jupyter Notebook..."
        echo "Acesse: http://localhost:8888"
        jupyter notebook exemplo_extracao.ipynb
        ;;
    4)
        echo ""
        echo "Executando todos os testes..."
        echo ""
        echo "1. Validação CNJ:"
        python3 validacao_cnj.py
        echo ""
        echo "2. Teste de extração (modo demonstração):"
        python3 extrair_datajud.py
        ;;
    5)
        echo "Saindo..."
        exit 0
        ;;
    *)
        echo "Opção inválida!"
        exit 1
        ;;
esac

echo ""
echo "✓ Execução concluída!"
echo ""
echo "Os resultados foram salvos em: resultados/"
echo "Os logs foram salvos em: logs/"
echo ""
