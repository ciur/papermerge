from .base import *
from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

DEBUG = True
# debug variable in templates is available only if INTERNAL_IPS are set
# to a not empty list
INTERNAL_IPS = ['127.0.0.1', ]

SITE_ID = 1
SECRET_KEY = get_random_string(50, chars)
MEDIA_ROOT = "/home/vagrant/papermerge-proj/run/media"
STORAGE_ROOT = "local:/home/vagrant/papermerge-proj/run/media"
S3 = False
OCR = True

CELERY_BROKER_URL = "memory://"

STATIC_ROOT = '/home/vagrant/papermerge-js/static/'

# write email messages in development mode to email spec by
# EMAIL_FILE_PATH
EMAIL_FILE_PATH = ""
EMAIL_BACKEND = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbname',
        'USER': 'dbuser',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 5432,
    },
}
