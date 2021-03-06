import dj_database_url

from .base import *

DEBUG = False

PRODUCTION = True

INSTALLED_APPS += ['storages']

ALLOWED_HOSTS += ['hellworld-editor.herokuapp.com']

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = None

STATIC_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
STATICFILES_STORAGE = 'hellworld.storage_backends.StaticStorage'

PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'hellworld.storage_backends.PublicMediaStorage'

PRIVATE_MEDIA_LOCATION = 'private'
PRIVATE_FILE_STORAGE = 'hellworld.storage_backends.PrivateMediaStorage'

BROKER_URL = os.environ.get('REDIS_URL')
CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

ADMINS = (('Matúš Zeleňák', 'matus.zelenak.gjh@gmail.com'), )
