#!/bin/sh

while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 10
done

poetry run python manage.py flush --no-input
poetry run python manage.py migrate

if [ "$TESTING" = "1" ]
then
    poetry run pytest
else
    DJANGO_SUPERUSER_PASSWORD=12345 poetry run python manage.py createsuperuser --username admin --email admin@email.com --noinput
    poetry run python manage.py runserver 0.0.0.0:8000
fi


exec "$@"