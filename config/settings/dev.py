from .base import *  # noqa

DEBUG = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mg-handler': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'papermerge': {
            'handlers': ['mg-handler'],
            'level': 'DEBUG'
        },
        'pmworker': {
            'handlers': ['mg-handler'],
            'level': 'DEBUG'
        },
        'mglib': {
            'handlers': ['mg-handler'],
            'level': 'DEBUG'
        },
    },
}
