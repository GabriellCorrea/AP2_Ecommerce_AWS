#!/usr/bin/env bash
# Bootstrap do ambiente de desenvolvimento local
set -e

echo "=== 1. Criando ambiente virtual ==="
python -m venv venv

echo "=== 2. Instalando dependências ==="
venv/bin/pip install -r requirements.txt -q

echo "=== 3. Configurando variáveis de ambiente ==="
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Arquivo .env criado a partir do .env.example — edite as credenciais se necessário."
fi

echo "=== 4. Subindo banco de dados MySQL via Docker ==="
if ! docker ps --format '{{.Names}}' | grep -q "^mysql-dev$"; then
  docker run -d --name mysql-dev \
    -e MYSQL_ROOT_PASSWORD=root \
    -e MYSQL_DATABASE=ecommerce_dev \
    -p 3306:3306 mysql:8
  echo "Aguardando MySQL inicializar..."
  until docker exec mysql-dev mysql -uroot -proot -e "SELECT 1" &>/dev/null; do
    sleep 2
  done
  sleep 2
else
  echo "Container mysql-dev já está rodando."
fi

echo "=== 5. Rodando migrations ==="
venv/bin/python manage.py migrate

echo "=== 6. Coletando arquivos estáticos ==="
venv/bin/python manage.py collectstatic --noinput

echo ""
echo "=== Setup concluído! ==="
echo ""
echo "Para criar o superusuário admin:"
echo "  venv/bin/python manage.py createsuperuser"
echo ""
echo "Para iniciar o servidor:"
echo "  venv/bin/python manage.py runserver"
echo ""
echo "API disponível em: http://127.0.0.1:8000/api/"
echo "Admin disponível em: http://127.0.0.1:8000/admin/"
