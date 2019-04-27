#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial
python manage.py collectstatic

gunicorn --bind 0.0.0.0:$PORT hellworld.wsgi --log-level DEBUG --access-logfile - --log-file -
