# coding: utf-8
import os
from pathlib import Path
from mglib.utils import try_load_config
import logging


logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PLACES = [
    "/etc/papermerge.conf.py",
    "papermerge.conf.py"
]

DEFAULT_PAPERMERGE_CONFIG_ENV_NAME = "PAPERMERGE_CONFIG"

cfg_papermerge = try_load_config(
    config_locations=DEFAULT_CONFIG_PLACES,
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
    "METADATA_PLUGINS", []
)

PAPERMERGE_METADATA_PLUGIN_MAPS = cfg_papermerge.get(
    "METADATA_PLUGIN_MAPS", {}
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

BINARY_FILE = cfg_papermerge.get(
    "BINARY_FILE",
    "/usr/bin/file"
)

BINARY_CONVERT = cfg_papermerge.get(
    "BINARY_CONVERT",
    "/usr/bin/convert"
)

BINARY_PDFTOPPM = cfg_papermerge.get(
    "BINARY_PDFTOPPM",
    "/usr/bin/pdftoppm"
)

BINARY_PDFINFO = cfg_papermerge.get(
    "BINARY_PDFINFO",
    "/usr/bin/pdfinfo"
)

BINARY_IDENTIFY = cfg_papermerge.get(
    "BINARY_IDENTIFY",
    "/usr/bin/identify"
)

BINARY_OCR = cfg_papermerge.get(
    "BINARY_OCR",
    "/usr/bin/tesseract"
)

BINARY_PDFTK = cfg_papermerge.get(
    "BINARY_PDFTK",
    "/usr/bin/pdftk"
)

AUTH_USER_MODEL = "core.User"

WSGI_APPLICATION = 'config.wsgi.application'
ROOT_URLCONF = 'config.urls'

# defines extra URL conf to be included
EXTRA_URLCONF = []


INSTALLED_APPS = [
    'rest_framework',
    'knox',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'papermerge.core',
    'papermerge.contrib.admin',
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
    'mgclipboard'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # mgclipboard.middleware.ClipboardMiddleware must be AFTER
    # * django.contrib.sessions.middleware
    # * django.contrib.auth.middleware
    'mgclipboard.middleware.ClipboardMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

PAPERMERGE_LANGUAGE_FROM_AGENT = cfg_papermerge.get(
    "LANGUAGE_FROM_AGENT", False
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
                'papermerge.contrib.admin.context_processors.extras',
                'papermerge.contrib.admin.context_processors.user_perms',
                'papermerge.contrib.admin.context_processors.user_menu',
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
    ('de', 'Deutsch'),
    ('en', 'English'),
]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = cfg_papermerge.get(
    "LANGUAGE_CODE",
    'en'
)

LOCALE_PATHS = (
    PROJ_ROOT / Path('papermerge'),
)

DATE_FORMAT = '%d/%m/%Y'
DATE_INPUT_FORMATS = ['%d/%m/%Y']

ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"

MEDIA_URL = '/documents/'

ALLOWED_HOSTS = [
    '*',
]

AUTH_MECHANISM = cfg_papermerge.get("AUTH_MECHANISM", "NodeAuthBackend")
logger.info("Using %s for user authentication." % AUTH_MECHANISM)

if AUTH_MECHANISM == "LdapAuthBackend":
    try:
        import ldap
        from django_auth_ldap.config import LDAPSearch, PosixGroupType, MemberDNGroupType, NestedMemberDNGroupType

        AUTH_LDAP_SERVER_URI = cfg_papermerge.get("LDAP_SERVER_URI")
        AUTH_LDAP_BIND_DN = cfg_papermerge.get("LDAP_BIND_DN")
        AUTH_LDAP_BIND_PASSWORD = cfg_papermerge.get("LDAP_BIND_PASSWORD")
        AUTH_LDAP_USER_SEARCH = LDAPSearch(
            cfg_papermerge.get("LDAP_USER_SEARCH_BASE"), ldap.SCOPE_SUBTREE, cfg_papermerge.get("LDAP_USER_SEARCH_FILTER")
        )

        _user_attr_map = cfg_papermerge.get("LDAP_USER_ATTR_MAP")
        if _user_attr_map is not None:
            AUTH_LDAP_USER_ATTR_MAP = _user_attr_map

        AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
            cfg_papermerge.get("LDAP_GROUP_SEARCH_BASE"),
            ldap.SCOPE_SUBTREE,
            cfg_papermerge.get("LDAP_GROUP_SEARCH_FILTER"),
        )
        AUTH_LDAP_USER_FLAGS_BY_GROUP = {
            "is_active": cfg_papermerge.get("LDAP_GROUP_ACTIVE"),
            "is_staff": cfg_papermerge.get("LDAP_GROUP_STAFF"),
            "is_superuser": cfg_papermerge.get("LDAP_GROUP_SUPERUSER"),
        }

        _group_type = cfg_papermerge.get("LDAP_GROUP_TYPE", "PosixGroupType")
        _group_type_name_attr = cfg_papermerge.get("LDAP_GROUP_TYPE_NAME_ATTR", "cn")
        _group_type_member_attr = cfg_papermerge.get("LDAP_GROUP_TYPE_MEMBER_ATTR", "cn")

        AUTH_LDAP_FIND_GROUP_PERMS = True

        if _group_type == "PosixGroupType":
            AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr= _group_type_name_attr)
        elif _group_type == "MemberDNGroupType":
            AUTH_LDAP_GROUP_TYPE = MemberDNGroupType(name_attr = _group_type_name_attr, member_attr = _group_type_member_attr)
        elif _group_type == "NestedMemberDNGroupType":
            AUTH_LDAP_GROUP_TYPE = NestedMemberDNGroupType(name_attr = _group_type_name_attr, member_attr = _group_type_member_attr)

    except ModuleNotFoundError as e:
        # As not all users want to use LDAP as their authentication provider, we need to wrap the imports (as they might not be available)
        logger.warning(
            "Could not import module '%s'. LDAP authentication is configured but couldn't be enabled. "
            "Please check whether you installed the ldap.txt requirements file. "
            "The authentication will be set to NodeAuthBackend." % e.name)
        AUTH_MECHANISM = "NodeAuthBackend"


AUTHENTICATION_BACKENDS = (
    'papermerge.core.auth.' + AUTH_MECHANISM,
    'allauth.account.auth_backends.AuthenticationBackend'
)


ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/accounts/login/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/admin/browse/'


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'

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


# TASK_QUEUE_DIR is used
# in conjunction with CELERY_BROKER_URL = "filesystem://"
# This settings (TASK_QUEUE_DIR + filesystem as broker) is very convinient
# in development environment.
PAPERMERGE_TASK_QUEUE_DIR = cfg_papermerge.get(
    "TASK_QUEUE_DIR",
    os.path.join(PROJ_ROOT, "queue")
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

# For each user create a specil folder called Inbox
# Useful only in dev/production (must be False in testing environment)
PAPERMERGE_CREATE_INBOX = True

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
