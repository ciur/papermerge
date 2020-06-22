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

Configuration file uses python syntax.


Some of the most used configurations which you might be interest in:
  
    * :ref:`media_dir` - location where all uploaded/imported documents are stored
    *
  

Paths and Folders
##################

.. _db_dir:

DB_DIR
~~~~~~~

* ``/path/to/papermerge/sqlite/db/``

Defines location where db.sqlite3 will be saved.
By default uses project's local directory.

Example::
    
    DB_DIR = "/opt/papermerge/db/"

.. _media_dir:

MEDIA_DIR
~~~~~~~~~~~

  * ``/path/to/media/``

  Defines directory where all uploaded documents will be stored.

  By default uses a folder named ``media`` in project's local directory.

.. _static_dir:

STATIC_DIR
~~~~~~~~~~

 * ``/path/to/collected/static/assets/``

  Location where all static assets of the project Papermerge project (javascript files, css files) will be copied by ``./manage collectstatic`` command.

  By default uses a folder named `static` in project's local directory.

  Example::
      
    STATIC_DIR = "/opt/papermerge/static/"



Document Importer
##################

Importer is a command line utility, which you can invoke with ``./manage.py importer``, used to import all documents
from local directory.

.. _importer_dir:

IMPORTER_DIR
~~~~~~~~~~~~

 * ``/path/where/documents/will/be/imported/from/``

  Location on local file system where Papermerge 
  will try to import documents from.

  IMPORTER_DIR = "/opt/papermerge/import/"



MG_OCR_LANGUAGES
~~~~~~~~~~~~~~~~~

  Addinational languages for text OCR. A dictionary where key is `ISO 639-2/T code <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_ and value is name of postgresql language dictionary.

  Example::

    MG_OCR_LANGUAGES = {
        'heb': 'hebrew',
        'jpn': 'japanese'
    }

Note that both `hebrew` and `japanes` must be listed in Name column of `\\dF` command in psql (which basically means that postgres dictionaries `hebrew` and `japanes` are installed).
