import os
from os.path import expanduser

from .base import *

DEBUG = True

SITE_ID = 1

# Special folders are those starting with DOT character.
# For example: .inbox, .trash
PAPERMERGE_CREATE_SPECIAL_FOLDERS = False

DATABASE_ROUTERS = []

INSTALLED_APPS = (
    'rest_framework',
    'knox',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'papermerge.core',
    'papermerge.contrib.admin',
    'papermerge.test',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dynamic_preferences',
    # comment the following line if you don't want to use user preferences
    'dynamic_preferences.users.apps.UserPreferencesConfig',
    'polymorphic_tree',
    'polymorphic',
    'mptt',
    'mgclipboard',
    'bootstrap4',
    'papermerge.test.parts.app_0',  # absolute minimum app
    'papermerge.test.parts.app_dr',  # data retention app
    'papermerge.test.parts.app_max_p',
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mgclipboard.middleware.ClipboardMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'papermerge.contrib.admin.middleware.TimezoneMiddleware'
]

AUTHENTICATION_BACKENDS = (
    'papermerge.test.auth_backends.TestcaseUserBackend',
    'papermerge.core.auth.NodeAuthBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

REST_KNOX = {
    'AUTH_TOKEN_CHARACTER_LENGTH': 32,
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
}


CELERY_BROKER_URL = "memory://"

# The default password hasher is rather slow by design.
# If you’re authenticating many users in your tests,
# you may want to use a custom settings file and set
# the PASSWORD_HASHERS setting to a faster hashing algorithm:
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'CRITICAL'
    },
}

MEDIA_ROOT = os.path.join(
    PROJ_ROOT,
    "papermerge",
    "test",
    "media"
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# guess where BINARY_STAPLER is located
if not BINARY_STAPLER:  # if BINARY_STAPLER was not set in papermerge.conf.py
    try:  # maybe it is in virtual environment?
        BINARY_STAPLER = f"{os.environ['VIRTUAL_ENV']}/bin/stapler"
    except Exception:
        # crude guess
        home_dir = expanduser('~')
        BINARY_STAPLER = f"{home_dir}/.local/bin/stapler"
