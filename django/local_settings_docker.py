from project.settings import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'REPLACE WITH REAL SECRET'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'gallery',
    'USER': 'gallery',
    'PASSWORD': 'gallery',
    'HOST': 'postgresql',
    'PORT': 5432,
  }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES['files'] = {
  'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
  'LOCATION': '/home/sid/cache',
}

MEDIA_ROOT = '/home/sid/mediaroot'

STATICFILES_DIRS += [
  '/home/sid/brython',
]

