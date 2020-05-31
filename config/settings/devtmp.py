# coding: utf-8
import os
from pathlib import Path
from .base import *

DEBUG = True
UNIT_TESTS = False
# debug variable in templates is available only if INTERNAL_IPS are set
# to a not empty list
INTERNAL_IPS = ['127.0.0.1', ]

SITE_ID = 1

SECRET_KEY = os.environ['SECRET_KEY']
MEDIA_ROOT = os.environ['MEDIA_ROOT']
STORAGE_ROOT = os.environ['STORAGE_ROOT']

CELERY_BROKER_URL = "filesystem://"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'data_folder_in': '',
    'data_folder_out': '',
    'data_folder_processed': ''
}
# write email messages in development mode to email spec by
# EMAIL_FILE_PATH
EMAIL_FILE_PATH = ""
EMAIL_BACKEND = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
    },
    'maildb': {
    }
}

#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'handlers': {
#        'console': {
#            'class': 'logging.StreamHandler',
#        }
#    },
#    'loggers': {
#        'django.db.backends': {
#            'handlers': ['console'],
#            'level': 'DEBUG'
#        },
#
#    },
#}

STATICFILES_DIRS = [
    '/home/eugen/github/papermerge-js/static'
]
