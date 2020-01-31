from .base import *

DEBUG = True
# debug variable in templates is available only if INTERNAL_IPS are set
# to a not empty list
INTERNAL_IPS = ['127.0.0.1', ]

SITE_ID = 1
SECRET_KEY = "VeryVeryVerySecretToken"
MEDIA_ROOT = "/home/vagrant/papermerge-proj/run/media"
STORAGE_ROOT = "local:/home/vagrant/papermerge-proj/run/media"
S3 = False
OCR = True

CELERY_BROKER_URL = "filesystem://"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'data_folder_in': '/home/vagrant/papermerge-proj/run/broker/data_in',
    'data_folder_out': '/home/vagrant/papermerge-proj/run/broker/data_in',
}

STATICFILES_DIRS = [
    '/home/vagrant/papermerge-js/static'
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
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 5432,
    },
}
