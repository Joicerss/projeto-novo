@echo off
REM Script de execução do pacote DataJud/CNJ (Windows)

echo ========================================
echo Pacote de Extração DataJud/CNJ
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python nao encontrado. Por favor, instale Python 3.11 ou superior.
    pause
    exit /b 1
)

echo [OK] Python encontrado
python --version

REM Verificar ambiente virtual
if not exist "venv" (
    echo.
    echo Criando ambiente virtual...
    python -m venv venv
    echo [OK] Ambiente virtual criado
)

REM Ativar ambiente virtual
echo.
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo [OK] Ambiente virtual ativado

REM Instalar dependências
echo.
echo Instalando dependencias...
pip install -q -r requirements.txt
echo [OK] Dependencias instaladas

REM Criar diretórios necessários
echo.
echo Criando diretorios...
if not exist "dados" mkdir dados
if not exist "resultados" mkdir resultados
if not exist "logs" mkdir logs
echo [OK] Diretorios criados

REM Verificar arquivo .env
if not exist ".env" (
    echo.
    echo [AVISO] Arquivo .env nao encontrado!
    echo Copiando .env.exemplo para .env...
    copy .env.exemplo .env
    echo [OK] Arquivo .env criado
    echo.
    echo ATENCAO: Configure suas credenciais no arquivo .env antes de continuar!
    echo Edite o arquivo .env e adicione sua chave API do DataJud.
    echo.
    pause
)

REM Menu
echo.
echo Escolha uma opcao:
echo.
echo 1. Executar validacao CNJ (teste)
echo 2. Executar extracao DataJud
echo 3. Abrir Jupyter Notebook
echo 4. Executar todos os testes
echo 5. Sair
echo.
set /p opcao="Opcao: "

if "%opcao%"=="1" (
    echo.
    echo Executando validacao CNJ...
    python validacao_cnj.py
) else if "%opcao%"=="2" (
    echo.
    echo Executando extracao DataJud...
    python extrair_datajud.py
) else if "%opcao%"=="3" (
    echo.
    echo Iniciando Jupyter Notebook...
    echo Acesse: http://localhost:8888
    jupyter notebook exemplo_extracao.ipynb
) else if "%opcao%"=="4" (
    echo.
    echo Executando todos os testes...
    echo.
    echo 1. Validacao CNJ:
    python validacao_cnj.py
    echo.
    echo 2. Teste de extracao (modo demonstracao):
    python extrair_datajud.py
) else if "%opcao%"=="5" (
    echo Saindo...
    exit /b 0
) else (
    echo Opcao invalida!
    pause
    exit /b 1
)

echo.
echo [OK] Execucao concluida!
echo.
echo Os resultados foram salvos em: resultados\
echo Os logs foram salvos em: logs\
echo.
pause
