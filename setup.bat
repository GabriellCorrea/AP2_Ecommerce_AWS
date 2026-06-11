@echo off
echo === 1. Criando ambiente virtual ===
python -m venv venv

echo === 2. Instalando dependencias ===
venv\Scripts\pip install -r requirements.txt -q

echo === 3. Configurando variaveis de ambiente ===
if not exist .env (
    copy .env.example .env
    echo Arquivo .env criado a partir do .env.example
)

echo === 4. Subindo banco de dados MySQL via Docker ===
docker ps --format "{{.Names}}" | findstr /x "mysql-dev" >nul 2>&1
if errorlevel 1 (
    docker run -d --name mysql-dev -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=ecommerce_dev -p 3306:3306 mysql:8
    echo Aguardando MySQL inicializar...
    :waitloop
    docker exec mysql-dev mysql -uroot -proot -e "SELECT 1" >nul 2>&1
    if errorlevel 1 (
        timeout /t 2 /nobreak >nul
        goto waitloop
    )
    timeout /t 2 /nobreak >nul
) else (
    echo Container mysql-dev ja esta rodando.
)

echo === 5. Rodando migrations ===
venv\Scripts\python manage.py migrate

echo === 6. Coletando arquivos estaticos ===
venv\Scripts\python manage.py collectstatic --noinput

echo.
echo === Setup concluido! ===
echo.
echo Para criar o superusuario admin:
echo   venv\Scripts\python manage.py createsuperuser
echo.
echo Para iniciar o servidor:
echo   venv\Scripts\python manage.py runserver
echo.
echo API disponivel em: http://127.0.0.1:8000/api/
echo Admin disponivel em: http://127.0.0.1:8000/admin/
