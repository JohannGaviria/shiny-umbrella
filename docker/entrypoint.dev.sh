#!/bin/sh

echo 'Waiting for database...'
python manage.py wait_for_db --settings=config.settings.development

echo 'Applying migrations...'
python manage.py makemigrations --settings=config.settings.development
python manage.py migrate --settings=config.settings.development

echo 'Running server...'
python manage.py runserver 0.0.0.0:8000 --settings=config.settings.development
