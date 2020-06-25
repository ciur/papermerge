# coding: utf-8
import os
from pathlib import Path
from mglib.utils import try_load_config

from django.utils.translation import gettext_lazy as _

DEFAULT_CONFIG_PLACES = [
    "/etc/papermerge.conf.py",
    "papermerge.conf.py"
]

DEFAULT_PAPERMERGE_CONFIG_ENV_NAME = "PAPERMERGE_CONFIG"

cfg_papermerge = try_load_config(
    config_locations=[
        "/etc/papermerge.conf.py",
        "papermerge.conf.py"
    ],
    config_env_var_name=DEFAULT_PAPERMERGE_CONFIG_ENV_NAME
)

# do not remove this assignment. It is used in core checks to
# figure out if papermerge configuration file was successfully load.
CFG_PAPERMERGE = cfg_papermerge

# project root directory
# 1. settings 2. config 3. papermerge-proj - parent 3x
PROJ_ROOT = Path(__file__).parent.parent.parent
DEBUG = True

SECRET_KEY = "87akjh34jh34-++JKJ8(this+is+papermerge!DMS!)"

SITE_ID = 1

STATIC_ROOT = cfg_papermerge.get(
    'STATIC_DIR', os.path.join(PROJ_ROOT, "static")
)

MEDIA_ROOT = cfg_papermerge.get(
    'MEDIA_DIR',
    os.path.join(PROJ_ROOT, "media")
)

STATIC_URL = cfg_papermerge.get(
    "STATIC_URL",
    "/static/"
)

MEDIA_URL = cfg_papermerge.get(
    "MEDIA_URL",
    "/media/"
)

# This is where Papermerge will look for PDFs to index
PAPERMERGE_IMPORTER_DIR = cfg_papermerge.get(
    "IMPORTER_DIR",
    None
)

PAPERMERGE_FILES_MIN_UNMODIFIED_DURATION = cfg_papermerge.get(
    "FILES_MIN_UNMODIFIED_DURATION",
    1
)

PAPERMERGE_IMPORTER_LOOP_TIME = cfg_papermerge.get(
    "IMPORTER_LOOP_TIME",
    5
)

PAPERMERGE_IMPORT_MAIL_HOST = cfg_papermerge.get(
    "IMPORT_MAIL_HOST", ""
)
PAPERMERGE_IMPORT_MAIL_USER = cfg_papermerge.get(
    "IMPORT_MAIL_USER", ""
)
PAPERMERGE_IMPORT_MAIL_PASS = cfg_papermerge.get(
    "IMPORT_MAIL_PASS", ""
)
PAPERMERGE_IMPORT_MAIL_INBOX = cfg_papermerge.get(
    "IMPORT_MAIL_INBOX", "INBOX"
)
PAPERMERGE_IMPORT_MAIL_SECRET = cfg_papermerge.get(
    "IMPORT_MAIL_SECRET", ""
)

PAPERMERGE_DEFAULT_FILE_STORAGE = cfg_papermerge.get(
    "DEFAULT_FILE_STORAGE",
    "mglib.storage.FileSystemStorage"
)

PAPERMERGE_SEARCH_BACKEND = cfg_papermerge.get(
    "SEARCH_BACKEND",
    "papermerge.search.backends.db.SearchBackend"
)

PAPERMERGE_METADATA_PLUGINS = cfg_papermerge.get(
    "PAPERMERGE_METADATA_PLUGINS", []
)

PAPERMERGE_METADATA_DATE_FORMATS = [
    'dd.mm.yy',
    'dd.mm.yyyy',
    'dd.M.yyyy'
]

PAPERMERGE_METADATA_CURRENCY_FORMATS = [
    'dd.cc',
    'dd,cc'
]

PAPERMERGE_METADATA_NUMERIC_FORMATS = [
    'dddd',
    'd,ddd',
    'd.ddd'
]

PAPERMERGE_OCR_DEFAULT_LANGUAGE = cfg_papermerge.get(
    "OCR_DEFAULT_LANGUAGE",
    "deu"  # if not defined, defaults to German a.k.a Deutsch
)

PAPERMERGE_OCR_LANGUAGES = cfg_papermerge.get(
    "OCR_LANGUAGES",
    {
        "deu": "Deutsch",
        "eng": "English",
    }
)

PAPERMERGE_OCR_BINARY = cfg_papermerge.get(
    "OCR_BINARY",
    "/usr/bin/tesseract"
)

AUTH_USER_MODEL = "core.User"

WSGI_APPLICATION = 'config.wsgi.application'
ROOT_URLCONF = 'config.urls'


INSTALLED_APPS = (
    'rest_framework',
    'knox',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'papermerge.boss',
    'papermerge.core',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dynamic_preferences',
    # comment the following line if you don't want to use user preferences
    'dynamic_preferences.users.apps.UserPreferencesConfig',
    'polymorphic_tree',
    'polymorphic',
    'mptt',
    # we use postgres full text search
    'django.contrib.postgres',
    'anymail',
    'django_extensions',
    'mgclipboard'
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # mgclipboard.middleware.ClipboardMiddleware must be AFTER
    # * django.contrib.sessions.middleware
    # * django.contrib.auth.middleware
    'mgclipboard.middleware.ClipboardMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJ_ROOT / Path('config') / Path('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dynamic_preferences.processors.global_preferences',
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(
            cfg_papermerge.get(
                "DBDIR",
                PROJ_ROOT
            ),
            "db.sqlite3"
        )
    }
}

if cfg_papermerge.get("DBUSER", False):
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": cfg_papermerge.get("DBNAME", "papermerge"),
        "USER": cfg_papermerge.get("DBUSER"),
    }
    DATABASES["default"]["PASSWORD"] = cfg_papermerge.get("DBPASS", "")
    DATABASES["default"]["HOST"] = cfg_papermerge.get("DBHOST", "localhost")
    DATABASES["default"]["PORT"] = cfg_papermerge.get("DBPORT", 5432)


FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler'
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (
    PROJ_ROOT / Path('papermerge'),
)

DATE_FORMAT = '%d/%m/%Y'
DATE_INPUT_FORMATS = ['%d/%m/%Y']

ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True

LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'


MEDIA_URL = '/documents/'

ALLOWED_HOSTS = [
    '*',
]

AUTHENTICATION_BACKENDS = (
    'papermerge.core.auth.NodeAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
# Determines the e-mail verification method during signup – choose one of
# "mandatory", "optional", or "none". When set to “mandatory” the user is
# blocked from logging in until the email address is verified. Choose “optional”
# or “none” to allow logins with an unverified e-mail address. In case of
# “optional”, the e-mail verification mail is still sent, whereas in case of
# “none” no e-mail verification mails are sent.
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/login/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/boss/'


LOGIN_REDIRECT_URL = '/boss/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

STATIC_URL = '/static/'

# Pixel height used by PDFTOPPM utility. It means basically
# that all generated images will be of following heights only
# min_height, min_height + step, min_height + 2*step, ..., max_height
# When zoomin in and out, uility cycles through these values.
PDFTOPPM_STEP = 100
PDFTOPPM_MIN_HEIGHT = 100
PDFTOPPM_DEFAULT_HEIGHT = 900
PDFTOPPM_MAX_HEIGHT = 1500
# Value must be an integer from 1 to 100
# This values trades off quality agains size/complexity
# 100 - is perfect quality jpeg image, but larger in size
# 1 - poorest quality jpeg image - uses smallest amount of space
PDFTOPPM_JPEG_QUALITY = 90

# = 1 GB of space per tenant
MAX_STORAGE_SIZE = 1 * 1024 * 1024

UPLOAD_FILE_SIZE_MAX = 12 * 1024 * 1024
UPLOAD_FILE_SIZE_MIN = 1
UPLOAD_ALLOWED_MIMETYPES = ['application/pdf']

PAPERMERGE_TASK_QUEUE_DIR = cfg_papermerge.get(
    "TASK_QUEUE_DIR",
    os.path.join(PROJ_ROOT, "queue")
)

if not os.path.exists(
    PAPERMERGE_TASK_QUEUE_DIR
):
    os.makedirs(
        PAPERMERGE_TASK_QUEUE_DIR, exist_ok=True
    )

CELERY_BROKER_URL = "filesystem://"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'data_folder_in': PAPERMERGE_TASK_QUEUE_DIR,
    'data_folder_out': PAPERMERGE_TASK_QUEUE_DIR,
}

CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_WORKER_CONCURENCY = 1
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_TASK_DEFAULT_EXCHANGE = 'papermerge'
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'papermerge'

CELERY_INCLUDE = 'papermerge.core.tasks'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_TASK_RESULT_EXPIRES = 86400

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
