from project.settings import *

from os import getenv

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'REPLACE WITH REAL SECRET'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': getenv('POSTGRES_DB'),
    'USER': getenv('POSTGRES_USER'),
    'PASSWORD': getenv('POSTGRES_PASSWORD'),
    'HOST': getenv('POSTGRES_HOST'),
    'PORT': getenv('POSTGRES_PORT', 5432),
  }
}

CACHES['files'] = {
  'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
  'LOCATION': '/home/sid/cache',
}

MEDIA_ROOT = '/home/sid/upload'

STATICFILES_DIRS += [
  '/home/sid/brython',
]

