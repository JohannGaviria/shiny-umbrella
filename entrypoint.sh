#!/bin/sh

echo 'Applying migrations...'
python manage.py wait_for_db --settings=config.settings.production
python manage.py makemigrations --settings=config.settings.production
python manage.py migrate --settings=config.settings.production

echo 'Creating staticfiles...'
python manage.py collectstatic --noinput --settings=config.settings.production

echo 'Running server...'
gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.production config.wsgi:application --bind 0.0.0.0:$PORT