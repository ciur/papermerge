from .base import *  # noqa

DEBUG = True

INSTALLED_APPS.extend(
    ['django_extensions']
)

INTERNAL_IPS = ['127.0.0.1', ]

CORS_ALLOW_ALL_ORIGINS = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'papermerge': {
            'class': 'logging.FileHandler',
            'filename': 'papermerge.log',
            'level': 'DEBUG'
        },
    },
    'loggers': {
        'papermerge': {
            'handlers': ['papermerge'],
            'level': 'DEBUG'
        },
    },
}

PAPERMERGE_DEFAULT_FILE_STORAGE = "papermerge.storage.S3Storage"
PAPERMERGE_FILE_STORAGE_KWARGS = {
    'bucketname': 'dev-papermerge',
    'namespace': 'demo'
}
