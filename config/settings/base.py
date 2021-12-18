# coding: utf-8
import os

from pathlib import Path
from corsheaders.defaults import default_headers as default_cors_headers
from configula import Configula


cfg_papermerge = Configula(
    prefix="PAPERMERGE",
    config_locations=[
        "/etc/papermerge.conf.py",
        "papermerge.conf.py"
    ],
    config_env_var_name="PAPERMERGE_CONFIG"
)

# do not remove this assignment. It is used in core checks to
# figure out if papermerge configuration file was successfully load.
CFG_PAPERMERGE = cfg_papermerge

# project root directory
# 1. settings 2. config 3. papermerge-proj - parent 3x
PROJ_ROOT = Path(__file__).parent.parent.parent
DEBUG = True

SECRET_KEY = "87akjh34jh34-++JKJ8(this+is+papermerge!DMS!)"
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

SITE_ID = 1

STATIC_ROOT = cfg_papermerge.get(
    'static',
    'dir',
    default=os.path.join(PROJ_ROOT, "static")
)

STATIC_URL = cfg_papermerge.get(
    'static',
    'dir',
    default='/static/'
)

MEDIA_ROOT = cfg_papermerge.get(
    'media',
    'dir',
    default=os.path.join(PROJ_ROOT, "media")
)

MEDIA_URL = cfg_papermerge.get(
    'media',
    'url',
    default='/media/'
)


# This is where Papermerge will look for PDFs to index
PAPERMERGE_IMPORTER_DIR = cfg_papermerge.get(
    "IMPORTER_DIR",
    None
)

PAPERMERGE_FILES_MIN_UNMODIFIED_DURATION = cfg_papermerge.get_var(
    "FILES_MIN_UNMODIFIED_DURATION",
    1
)

PAPERMERGE_IMPORTER_LOOP_TIME = cfg_papermerge.get_var(
    "IMPORTER_LOOP_TIME",
    5
)


PAPERMERGE_OCR_DEFAULT_LANGUAGE = cfg_papermerge.get(
    'ocr',
    'default_language',
    default='deu'
)

PAPERMERGE_OCR_LANGUAGES = cfg_papermerge.get(
    'ocr',
    'language',
    default={
        'deu': 'Deutsch',
        'eng': 'English',
    }
)

PAPERMERGE_METADATA_DATE_FORMATS = [
    'dd.mm.yy',
    'dd.mm.yyyy',
    'dd.M.yyyy',
    'month'  # Month as locale’s full name, January, February
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

PAPERMERGE_MIMETYPES = [
    'application/octet-stream',
    'application/pdf',
    'image/png',
    'image/jpeg',
    'image/jpg',
    'image/tiff'
]

AUTH_USER_MODEL = "core.User"

WSGI_APPLICATION = 'config.wsgi.application'
ROOT_URLCONF = 'config.urls'
ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# defines extra URL conf to be included
EXTRA_URLCONF = []


INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_json_api',
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'papermerge.core.apps.CoreConfig',
    'papermerge.wsignals.apps.WsignalsConfig',
    'papermerge.notifications.apps.NotificationsConfig',
    'django.contrib.contenttypes',
    'dynamic_preferences',
    # comment the following line if you don't want to use user preferences
    'dynamic_preferences.users.apps.UserPreferencesConfig',
    'polymorphic_tree',
    'polymorphic',
    'mptt',
    'channels',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'papermerge.core.middleware.TimezoneMiddleware'
]

PAPERMERGE_LANGUAGE_FROM_AGENT = cfg_papermerge.get_var(
    'language_from_agent', False
)

if PAPERMERGE_LANGUAGE_FROM_AGENT:
    # django middle ware sets language code from agent 'Accept-Language'
    # header
    MIDDLEWARE.append(
        'django.middleware.locale.LocaleMiddleware'
    )

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

DATABASES = cfg_papermerge.get_django_databases(proj_root=PROJ_ROOT)

if cfg_papermerge.has_mysql:
    # Requires MySQL > 5.7.7 or innodb_large_prefix set to on
    SILENCED_SYSTEM_CHECKS = ['mysql.E001']

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler'
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

LANGUAGES = [
    ('de', 'Deutsch'),
    ('en', 'English'),
    ('fr', 'Français'),
]
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = cfg_papermerge.get_var(
    'language_code',
    default='en'
)

LOCALE_PATHS = (
    PROJ_ROOT / Path('papermerge'),
)

DATE_FORMAT = '%d/%m/%Y'
DATE_INPUT_FORMATS = ['%d/%m/%Y']

MEDIA_URL = '/documents/'

ALLOWED_HOSTS = [
    '*',
]


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
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


# TASK_QUEUE_DIR is used
# in conjunction with CELERY_BROKER_URL = "filesystem://"
# This settings (TASK_QUEUE_DIR + filesystem as broker) is very convinient
# in development environment.
PAPERMERGE_TASK_QUEUE_DIR = cfg_papermerge.get_var(
    'TASK_QUEUE_DIR',
    default=os.path.join(PROJ_ROOT, 'queue')
)

# even if other than filesystem message brokers will be used
# TASK_QUEUE_DIR queue dir will be created. This is because, at this point
# django cannot tell if CELERY_BROKER_URL will stay filesystem:// or it
# will change later (e.g. in production.py which inherits from base.py)
if not os.path.exists(
    PAPERMERGE_TASK_QUEUE_DIR
):
    os.makedirs(
        PAPERMERGE_TASK_QUEUE_DIR, exist_ok=True
    )

# For each user create a specil folders (e.g. Inbox, Trash)
# Useful only in dev/production (must be False in testing environment)
PAPERMERGE_CREATE_SPECIAL_FOLDERS = True

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
        'rest_framework.authentication.TokenAuthentication',
    ],
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_json_api.pagination.JsonApiPageNumberPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.JSONRenderer',
        # If you're performance testing, you will want to use the browseable API
        # without forms, as the forms can generate their own queries.
        # If performance testing, enable:
        # 'example.utils.BrowsableAPIRendererWithoutForms',
        # Otherwise, to play around with the browseable API, enable:
        'rest_framework_json_api.renderers.BrowsableAPIRenderer'
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework_json_api.schemas.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_json_api.filters.OrderingFilter',
        'rest_framework_json_api.django_filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'SEARCH_PARAM': 'filter[search]',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'
}

# available settings with their default values
DYNAMIC_PREFERENCES = {

    # a python attribute that will be added to model instances with preferences
    # override this if the default collide with one of your
    # models attributes/fields
    'MANAGER_ATTRIBUTE': 'preferences',

    # The python module in which registered preferences will be
    # searched within each app
    'REGISTRY_MODULE': 'preferences',

    # Allow quick editing of preferences directly in admin list view
    # WARNING: enabling this feature can cause data corruption
    # if multiple users
    # use the same list view at the same time,
    # see https://code.djangoproject.com/ticket/11313
    'ADMIN_ENABLE_CHANGELIST_FORM': False,

    # Customize how you can access preferences from managers. The default is to
    # separate sections and keys with two underscores.
    # This is probably not a settings you'll
    # want to change, but it's here just in case
    'SECTION_KEY_SEPARATOR': '__',

    # Use this to disable caching of preference.
    # This can be useful to debug things
    'ENABLE_CACHE': True,

    # Use this to disable checking preferences names.
    # This can be useful to debug things
    'VALIDATE_NAMES': True,
}

CORS_ALLOW_HEADERS = list(default_cors_headers) + [
    "Authorization",
    "Content-Disposition",
]
