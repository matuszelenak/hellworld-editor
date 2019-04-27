from .base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hellworld',
        'USER': 'hellworld',
        'HOST': 'db',
        'PORT': 5432
    }
}

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
