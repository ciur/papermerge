import os
from .base import *  # noqa

DEBUG = False
# debug variable in templates is available only if INTERNAL_IPS are set
# to a not empty list
INTERNAL_IPS = [
    '127.0.0.1',
]

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'dbname'),
        'USER': os.environ.get('POSTGRES_USER', 'dbuser'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'dbpass'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file_worker': {
            'class': 'logging.FileHandler',
            'filename': 'worker.log',
        },
        'file_app': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
        },
    },
    'loggers': {
        'mglib': {
            'handlers': ['file_app'],
            'level': 'DEBUG'
        },
        'papermerge': {
            'handlers': ['file_app'],
            'level': 'DEBUG'
        },
        'celery': {
            'handlers': ['file_worker'],
            'level': 'INFO'
        },
    },
}

PAPERMERGE_IMPORT_MAIL_HOST=os.environ.get('IMPORT_MAIL_HOST', '')
PAPERMERGE_IMPORT_MAIL_USER=os.environ.get('IMPORT_MAIL_USER', '')
PAPERMERGE_IMPORT_MAIL_PASS=os.environ.get('IMPORT_MAIL_PASS', '')
PAPERMERGE_IMPORT_MAIL_INBOX=os.environ.get('IMPORT_MAIL_INBOX', '')
PAPERMERGE_IMPORT_MAIL_BY_USER=os.environ.get('IMPORT_MAIL_BY_USER', False)
PAPERMERGE_IMPORT_MAIL_BY_SECRET=os.environ.get('IMPORT_MAIL_BY_SECRET', False)
PAPERMERGE_IMPORT_MAIL_DELETE=os.environ.get('IMPORT_MAIL_DELETE', False)
