#!/bin/sh

python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb
python3 manage.py collectstatic --noinput
python3 manage.py compilemessages --ignore "*/site-packages/*"

# Create a superuser for easier development
DJANGO_SUPERUSER_USERNAME=${SUPERUSER_USER} \
DJANGO_SUPERUSER_PASSWORD=${SUPERUSER_PASS} \
python3 manage.py createsuperuser --noinput

echo "Running Django development server on port 8000"
exec python3 manage.py runserver 0.0.0.0:8000
