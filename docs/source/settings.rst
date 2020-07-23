Settings
=========

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
    * :ref:`ocr_languages` - user can select one of those languages to perform OCR
    * :ref:`ocr_default_language` - default language for OCR
  

Paths and Folders
##################

.. _db_dir:

``DB_DIR``
~~~~~~~~~~~

* ``/path/to/papermerge/sqlite/db/``

Defines location where db.sqlite3 will be saved.
By default uses project's local directory.

Example::
    
    DB_DIR = "/opt/papermerge/db/"

.. _media_dir:

``MEDIA_DIR``
~~~~~~~~~~~~~~

  * ``/path/to/media/``

  Defines directory where all uploaded documents will be stored.

  By default uses a folder named ``media`` in project's local directory.

.. _static_dir:

``STATIC_DIR``
~~~~~~~~~~~~~~~~

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

``IMPORTER_DIR``
~~~~~~~~~~~~~~~~~

 * ``/path/where/documents/will/be/imported/from/``

  Location on local file system where Papermerge 
  will try to import documents from.

  IMPORTER_DIR = "/opt/papermerge/import/"


OCR
####

.. _ocr_languages:

``OCR_LANGUAGES``
~~~~~~~~~~~~~~~~~

  Addinational languages for text OCR. A dictionary where key is `ISO 639-2/T code <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_ and value human
  text name for language

  Example::

    OCR_LANGUAGES = {
        'heb': 'hebrew',
        'jpn': 'japanese'
    }

Note that both `hebrew` and `japanes` language data for tesseract must be installed. You can check Tesseract's available languages with following command::

  $ tesseract --list-langs

Default value for OCR_LANGUAGES uses following value::

    OCR_LANGUAGES = {
        "deu": "Deutsch",  # German language
        "eng": "English",
      }

.. _ocr_default_language:

``OCR_DEFAULT_LANGUAGE``
~~~~~~~~~~~~~~~~~~~~~~~~~

By default Papermerge will use language specified with this option to perform OCR. Change this value for language used by majority of your documents.

  Example:

    OCR_DEFAULT_LANGUAGE = "spa"

Default value is "deu" (German language).

.. _ocr_binary:

``OCR_BINARY``
~~~~~~~~~~~~~~~~

Full path to tesseract binary/executable file.
Default value is::

  OCR_BINARY = "/usr/bin/tesseract"

.. _i18n:

I18n and Localization
#######################

``LANGUAGE_CODE``
~~~~~~~~~~~~~~~~~~~

This option specifies language of user interface.
There are two options:

* en - for user interface in English language
* de - for user interface in German language

English is default fallback i.e. if you don't specify anything
or specify unsupported language then English will be used.
Instead of ``en`` you can use ``en-US``, ``en-UK`` etc.
Instead of ``de`` you can use ``de-DE``, ``de-AT`` etc.
`See here <http://www.i18nguy.com/unicode/language-identifiers.html>`_ full least of all available language codes.
You can :ref:`translate Papermerge <translate>` to your own language.

.. _database:

Database
###########

By default, Papermerge uses SQLite3 database (which is a file located in :ref:`db_dir`). Alternatively
you can use PostgreSQL database. Following are options for PostgreSQL database connections.

 .. _dbuser:

``DBUSER``
~~~~~~~~~~~

DB user used for PostgreSQL database connection. If specified will automatically 'switch' from
sqlite3 to PostgreSQL database.

  Example:

    DBUSER = "john"

.. _dbname:

``DBNAME``
~~~~~~~~~~~

PostgreSQL database name.
Default value is papermerge.

.. _dbhost:

``DBHOST``
~~~~~~~~~~~
 
PostgreSQL database host.
Default value is localhost.

.. _dbport:

``DBPORT``
~~~~~~~~~~~
   
PostgreSQL database port. Port must be specified as integer number. No string quotes.

  Example:

    DBPORT = 5432

Default value is 5432.

.. _dbpass:

``DBPASS``
~~~~~~~~~~~
 
Password for connecting to PostgreSQL database
Default value is empty string.

.. _settings_email:

EMail
#######

You can import documents directly from email/IMAP account.

``IMPORT_MAIL_HOST``
~~~~~~~~~~~~~~~~~~~~~

IMAP Server host.


``IMPORT_MAIL_USER``
~~~~~~~~~~~~~~~~~~~~~

Email account/IMAP user.


``IMPORT_MAIL_PASS``
~~~~~~~~~~~~~~~~~~~~~~

Email account/IMAP password

``IMPORT_MAIL_INBOX``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

IMAP folder to read email from.
Default value for this settings is INBOX.

``IMPORT_MAIL_SECRET``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Any email sent to the target account that does not contain this text will be ignored.
