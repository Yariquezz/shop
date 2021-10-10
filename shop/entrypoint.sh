#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
echo "Makemigrations..."
python manage.py makemigrations
echo "Migrate..."
python manage.py migrate
echo "Create superuser..."
python manage.py createsuperuser --username=$DJANGO_SUPERUSER_ADMIN --email=$DJANGO_SUPERUSER_EMAIL
echo "Collectstatic..."
python manage.py collectstatic --no-input --clear

exec "$@"