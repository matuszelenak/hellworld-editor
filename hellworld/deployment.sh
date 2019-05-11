#!/bin/bash
python manage.py migrate
python manage.py loaddata initial
python manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:$PORT hellworld.wsgi --env DJANGO_SETTINGS_MODULE=hellworld.settings.production --log-level DEBUG --access-logfile - --log-file -
