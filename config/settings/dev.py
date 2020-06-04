from .base import *  # noqa

DEBUG = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
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
    },
}
