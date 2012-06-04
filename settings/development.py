from common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'USER': 'vagrant',
        'NAME': 'djangolms',                      # Or path to database file if using sqlite3.
    }
}

COMPRESS_ENABLED = True
COMPRESS_REBUILD_TIMEOUT = 1

CELERY_ALWAYS_EAGER = True

INSTALLED_APPS.append('devserver')
