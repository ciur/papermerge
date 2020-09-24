import os
from .base import *  # noqa

DEBUG = True

INSTALLED_APPS.extend(
    [
        'mgpayments'
    ]
)

EXTRA_URLCONF = [
    'mgpayments.urls'
]

MG_PAYMENTS_CLIENT = 'mgpayments.client.StripeClient'

STRIPE_PUBLISHABLE_KEY = os.environ.get(
    "STRIPE_PUBLISHABLE_KEY", "XYZ"
)
STRIPE_SECRET_KEY = os.environ.get(
    "STRIPE_SECRET_KEY", "ABC"
)
STRIPE_WEBHOOK_SIGNING_KEY = os.environ.get(
    "STRIPE_WEBHOOK_SIGNING_KEY", "XYZ"
)

HOSTED_SUBSCRIPTION_PROD_ID = os.environ.get(
    "HOSTED_SUBSCRIPTION_PROD_ID", "abc"
)
HOSTED_SUBSCRIPTION_PRICE_ID = os.environ.get(
    "HOSTED_SUBSCRIPTION_PRICE_ID", "abc"
)

PRO_SUPPORT_PROD_ID = os.environ.get(
    "PRO_SUPPORT_PROD_ID", "abc"
)
PRO_SUPPORT_PRICE_ID = os.environ.get(
    "PRO_SUPPORT_PRICE_ID", "abc"
)

INTERNAL_IPS = ['127.0.0.1', ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'papermerge': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'celery': {
            'handlers': ['papermerge'],
            'level': 'INFO'
        },
        'papermerge': {
            'handlers': ['papermerge'],
            'level': 'DEBUG'
        },
    },
}
