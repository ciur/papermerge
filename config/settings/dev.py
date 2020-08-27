from .base import *  # noqa

DEBUG = True

INTERNAL_IPS = ['127.0.0.1', ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'ocr.log',
            'level': 'DEBUG'
        },
    },
    'loggers': {
        'papermerge': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'papermerge.core.ocr': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
        'mglib': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
    },
}
