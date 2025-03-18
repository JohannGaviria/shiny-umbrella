#!/bin/sh

echo 'Waiting for database...'
python manage.py wait_for_db --settings=config.settings.production

echo 'Applying migrations...'
python manage.py makemigrations --settings=config.settings.production
python manage.py migrate --settings=config.settings.production

echo 'Creating staticfiles...'
python manage.py collectstatic --no-input --settings=config.settings.production

echo 'Running server...'
gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.production config.wsgi:application --bind 0.0.0.0:$PORT