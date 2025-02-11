#!/bin/sh

echo "=== MAKING MIGRATIONS ==="
python manage.py makemigrations
echo "=== ALL MIGRATIONS ==="
python manage.py showmigrations
echo "=== APPLYING MIGRATIONS ==="
python manage.py migrate --run-syncdb
echo "=== DEPLOYING STATIC FILES ==="
python manage.py collectstatic --noinput
echo "=== COMPILING TRANSLATIONS ==="
python manage.py compilemessages --ignore "*/site-packages/*"
echo "=== CREATING SUPERUSER ==="
DJANGO_SUPERUSER_USERNAME=${SUPERUSER_USER} \
DJANGO_SUPERUSER_PASSWORD=${SUPERUSER_PASS} \
python manage.py createsuperuser --noinput
echo "=== STARTING SERVER... ==="
exec python -m gunicorn --bind 0.0.0.0:8000 langate.asgi:application -k uvicorn.workers.UvicornWorker
