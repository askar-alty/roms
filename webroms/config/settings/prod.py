from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'roms_db',
        'USER': 'roms_user',
        'PASSWORD': 'roms_pwd',
        'HOST': 'postgres',
        'PORT': '5432'
    }
}

ALLOWED_HOSTS = ['*']