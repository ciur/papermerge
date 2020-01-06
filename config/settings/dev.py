# coding: utf-8
from .base import *

DEBUG = True
UNIT_TESTS = False
# debug variable in templates is available only if INTERNAL_IPS are set
# to a not empty list
INTERNAL_IPS = ['127.0.0.1', ]

SECRET_KEY = ""
SITE_ID = 1
MEDIA_ROOT = ""

CELERY_BROKER_URL = "filesystem://"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'data_folder_in': '',
    'data_folder_out': '',
    'data_folder_processed': ''
}

STORAGE_ROOT = ''

# write email messages in development mode to email spec by
# EMAIL_FILE_PATH
EMAIL_FILE_PATH = ""
EMAIL_BACKEND = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'maildb': {
    }
}
