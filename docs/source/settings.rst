Settings
=========

.. warning::

    Starting with version 1.3.0 configuration process will be simplified
    and parts of this documentation page will become absolete.

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


.. _STORAGE_ROOT:

STORAGE_ROOT
~~~~~~~~~~~~

* ``local:/<path to local folder>``
* ``s3:/<path to bucket>``

Defines either local or a remote location where documents are stored. In case of local, it's meaning
is same of for Django's ``MEDIA_ROOT``. In case of s3 storage it indicates path to the S3 bucket.

Examples::
    
    STORAGE_ROOT = 'local:/home/vagrant/papermerge-proj/run/media'  # good for development env
    STORAGE_ROOT = 's3:/yourbucketname/alldocuments' # suitable for production

.. note::
    In case when you choose **not** to use S3 storage both ``STORAGE_ROOT`` needs to be
    set to ``local://...`` path **and** :ref:`S3` option must be set to False.
    And other way around, if you want to use S3 storage, both ``SOTRAGE_ROOT``
    and ``S3`` needs to be set accordingly (S3=True, STORAGE_ROOT='s3:/bucketname').

.. _s3:

S3
~~~

  * ``True|False``

  Instructs papermerge if you want to use S3 storage. ``S3=True`` is more suitable for production
  environments.

  .. note::
    In case ``S3=True`` you need to point ref:`STORAGE_ROOT` to s3 location.

.. _ocr:

OCR
~~~

 * ``True|False``

  Enables or disables OCR features. With ``OCR=False`` no workers needs to be configured;

.. _databases:

DATABASES
~~~~~~~~~

 This is Django specific configuration settings. Papermerge uses PostgreSQL as database, which
 means that ENGINE options must be set to ``django.db.backends.postgresql``.
 Example::

     DATABASES = {
         'default': {
             'NAME': 'db_name',
             'ENGINE': 'django.db.backends.postgresql',
             'USER': 'db_user',
             'PASSWORD': 'db_password'
         },
     }


.. _staticfilesdirs:

STATICFILES_DIRS
~~~~~~~~~~~~~~~~

  Include absolute path where papermege-js static files are.

  Example::

        STATICFILES_DIRS = [
            '/home/vagrant/papermerge-js/static'
        ]

.. _mg_ocr_languages:        

MG_OCR_LANGUAGES
~~~~~~~~~~~~~~~~~

  Addinational languages for text OCR. A dictionary where key is `ISO 639-2/T code <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_ and value is name of postgresql language dictionary.

  Example::

    MG_OCR_LANGUAGES = {
        'heb': 'hebrew',
        'jpn': 'japanese'
    }

Note that both `hebrew` and `japanes` must be listed in Name column of `\\dF` command in psql (which basically means that postgres dictionaries `hebrew` and `japanes` are installed).
