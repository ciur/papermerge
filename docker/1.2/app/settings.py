import os
from .base import *

DEBUG = True
# debug variable in templates is available only if INTERNAL_IPS are set
# to a not empty list
INTERNAL_IPS = ['127.0.0.1', ]

SITE_ID = 1
SECRET_KEY = "VeryVeryVerySecretToken"
MEDIA_ROOT = "/opt/media"
STORAGE_ROOT = "local:/opt/media"
S3 = False
OCR = True

CELERY_BROKER_URL = "filesystem://"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'data_folder_in': '/opt/broker/queue',
    'data_folder_out': '/opt/broker/queue',
}

STATICFILES_DIRS = [
    '/opt/papermerge-js/static'
]

# write email messages in development mode to email spec by
# EMAIL_FILE_PATH
EMAIL_FILE_PATH = ""
EMAIL_BACKEND = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbname',
        'USER': 'dbuser',
        'PASSWORD': 'dbpass',
        'HOST': 'db',
        'PORT': 5432,
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'papermerge': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'papermerge': {
            'handlers': ['papermerge'],
            'level': 'DEBUG'
        },
    },
}
