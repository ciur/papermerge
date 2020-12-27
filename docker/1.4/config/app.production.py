import os

from .base import *  # noqa


DEBUG = False
# debug variable in templates is available only if INTERNAL_IPS are set
# to a not empty list
INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS.extend(
    ['mod_wsgi.server', ]
)

ALLOWED_HOSTS = ['*']

CELERY_BROKER_URL = "redis://redis/0"
CELERY_BROKER_TRANSPORT_OPTIONS = {}
CELERY_RESULT_BACKEND = "redis://redis/0"

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
