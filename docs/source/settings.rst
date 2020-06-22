Settings
=========

.. warning::

    This page describes the new configurations way introduced in version 1.3.0 which
    will be available starting with July 2020. How to configure previous releases see version
    specific respective documentation.

Papermerge loads its settings from a configurations file. At first it tries to
read following files:

  1. /etc/papermerge.conf.py
  2. papermerge.conf.py - from current project directory

If neither of above files exists it will check environment variable
``PAPERMERGE_CONFIG_FILE``. In case environment variable
``PAPERMERGE_CONFIG_FILE`` points to an existing file - it will try to read
its configurations from there.

If all above attempts fail, Papermerge will use default configurations values
and issue you a warning. If you want to get rid of warning message, just create an
empty configuration file papermerge.conf.py in project root directory (right next to papermerge.conf.py.example) or in location /etc/papermerge.conf.py.


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
