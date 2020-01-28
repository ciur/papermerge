Settings
=========

These are configurations settings for Papermerge - Web App. Configuration
settings are used in same manner as `for any Django based project
<https://docs.djangoproject.com/en/3.0/topics/settings/>`_.

Settings which are common for all environments (production, development, staging)
are defined in ``papermerge.config.settings.base`` module.

If you want to reuse ``papermerge.config.settings.base``, create python file, for example
``staging.py``, and import all settings from base module::

    from .base import *

    DEBUG = False
    STATIC_ROOT = '/www/static/'

Example above assumes that ``staging.py`` was created in same folder with ``base.py``.
Don't forget to point `DJANGO_SETTINGS_MODULE <https://docs.djangoproject.com/en/3.0/topics/settings/#envvar-DJANGO_SETTINGS_MODULE>`_ environment variable to your settings module.
