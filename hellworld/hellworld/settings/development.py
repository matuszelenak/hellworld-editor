from celery.schedules import crontab

from .base import *


DEBUG = True

PRODUCTION = False

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

CELERY_BEAT_SCHEDULE = {
    # 'update_inputs': {
    #     'task': 'submit.tasks.UpdateTaskInputs',
    #     'schedule': crontab()  # execute every minute
    # }
}

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"

COMPILED_BINARIES_PATH = os.path.join(MEDIA_ROOT, 'compiled')

AWS_ACCESS_KEY_ID = 'AKIAZL4EH7Q3YL7BQNGP'
AWS_SECRET_ACCESS_KEY = 'n1+BuFLZKaRQW6rHH+Ggg+QR33U6d7j7X8XpsW4J'
AWS_STORAGE_BUCKET_NAME = 'hellworld-editor'
