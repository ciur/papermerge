.. _settings:

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


Main App, Worker or Both?
###########################

Some configuration variables are for worker only (the part which :ref:`OCRs <ocrs>` the
documents, imports documents form local directory or fetches them from
imap/email account), some configuration variables are for main app only and
some are for both. This distinction becomes aparent in case you deploy
main app and worker on separate hosts; another scenario when this distinction
**is important in case of containerized deployment via docker** - it so,
because usually main app and worker will run in different containers - and
thus will have different copies of papermerge.conf.py file.

The settings below specify for whom configuration settings is addressed. When
it says: "context: ``worker``" - it means variable applies only in context
of worker i.e. it needs to be changed in ``papermerge.conf.py`` on worker
instance/host/container.

When settings description states "context: ``main app, worker``" - it means
configuration needs to be changed **on both - main app and worker** in order to
function properly. 


Some of the most used configurations which you might be interest in:
  
    * :ref:`media_dir` - location where all uploaded/imported documents are stored
    * :ref:`ocr_languages` - user can select one of those languages to perform :ref:`OCR <ocr>`
    * :ref:`ocr_default_language` - default language for :ref:`OCR <ocr>`
  

Paths and Folders
##################

.. _db_dir:

``DBDIR``
~~~~~~~~~~~

* ``/path/to/papermerge/sqlite/db/``
* context: ``main app``

Defines location where db.sqlite3 will be saved.
By default uses project's local directory.

Example::
    
    DBDIR = "/opt/papermerge/db/"

.. _media_dir:

``MEDIA_DIR``
~~~~~~~~~~~~~~

  * ``/path/to/media/``
  * context: ``main app, worker``

  Defines directory where all uploaded documents will be stored.

  By default uses a folder named ``media`` in project's local directory.

.. _static_dir:

``STATIC_DIR``
~~~~~~~~~~~~~~~~

 * ``/path/to/collected/static/assets/``
 * context: ``main app``

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
 * context: ``worker``

  Location on local file system where Papermerge 
  will try to import documents from.

  IMPORTER_DIR = "/opt/papermerge/import/"


OCR
#####

.. _ocr_languages:

``OCR_LANGUAGES``
~~~~~~~~~~~~~~~~~

* context: ``main app, worker``

  Addinational languages for text :ref:`OCR <ocr>`. A dictionary where key is `ISO 639-2/T code <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_ and value human
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

* context: ``main app, worker``

By default Papermerge will use language specified with this option to perform :ref:`OCR <ocr>`. Change this value for language used by majority of your documents.

  Example:

    OCR_DEFAULT_LANGUAGE = "spa"

Default value is "deu" (German language).

.. _i18n:

I18n and Localization
#######################
.. _config_language_code:

``LANGUAGE_CODE``
~~~~~~~~~~~~~~~~~~~

* context: ``main app``

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

Default value: ``en``

.. _config_language_from_agent:

``LANGUAGE_FROM_AGENT``
~~~~~~~~~~~~~~~~~~~~~~~~

If is set to True, will use same language code as your Web Browser (agent) does.
Browsers send 'Accept-Language' header with their locale.
For more, `read here <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language>`_.

* If ``True``  - will override :ref:`LANGUAGE_CODE <config_language_code>` option. This means that with ``LANGUAGE_FROM_AGENT=True`` in whatever locale settings your Web Browser runs - same will be used by Papermerge instance.
* If ``False`` - language code specified in :ref:`LANGUAGE_CODE <config_language_code>` option will be used and 'Accept-Language' header in browser will be ignored.

Default value: ``False``

.. _database:

Database
###########

By default, Papermerge uses SQLite3 database (which is a file located in :ref:`db_dir`). Alternatively
you can use a PostgreSQL or MySQL/MariaDB database. Following are options for PostgreSQL and MySQL/MariaDB database connections.

 .. _dbtype:

``DBTYPE``
~~~~~~~~~~~

context: ``main app``

DB type (if different from SQLite3).
For PostgreSQL database use one of following values:

* pg
* postgre
* postgres
* postgresql

For MySQL/MariaDB database (they share same database backend) use one of following values:

* my
* mysql
* maria
* mariadb

  Example:

    DBTYPE = "mysql"

 .. _dbuser:

``DBUSER``
~~~~~~~~~~~

context: ``main app``

DB user used for database connection.

  Example:

    DBUSER = "john"

.. _dbname:

``DBNAME``
~~~~~~~~~~~

context: ``main app``

Database name.
Default value is papermerge.

.. _dbhost:

``DBHOST``
~~~~~~~~~~~

context: ``main app``
 
Database host.
Default value is localhost.

.. _dbport:

``DBPORT``
~~~~~~~~~~~

context: ``main app``
   
Database port. Port must be specified as integer number. No string quotes.

  Example:

    DBPORT = 5432

Default value is 5432 for PostgreSQL and 3306 for MySQL/MariaDB.

.. _dbpass:

``DBPASS``
~~~~~~~~~~~

context: ``main app``
 
Password for connecting to database
Default value is empty string.

.. _settings_email:

EMail
#######

You can import documents directly from email/IMAP account. All EMail importer settings must be defined in papermerge.conf.py on worker side.


``IMPORT_MAIL_HOST``
~~~~~~~~~~~~~~~~~~~~~

context: ``worker``

IMAP Server host.


``IMPORT_MAIL_USER``
~~~~~~~~~~~~~~~~~~~~~

context: ``worker``

Email account/IMAP user.


``IMPORT_MAIL_PASS``
~~~~~~~~~~~~~~~~~~~~~~

context: ``worker``

Email account/IMAP password.

``IMPORT_MAIL_INBOX``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

context: ``worker``

IMAP folder to read email from.
Default value for this settings is INBOX.

``IMPORT_MAIL_BY_USER``
~~~~~~~~~~~~~~~~~~~~~~~~~~

context: ``worker``

Whether to allow users to receive in their inbox folder
emails sent from their own email address.

``IMPORT_MAIL_BY_SECRET``
~~~~~~~~~~~~~~~~~~~~~~~~~~

context: ``worker``

Whether to allow users to receive in their inbox folder
emails containing their own secret.

``IMPORT_MAIL_DELETE``
~~~~~~~~~~~~~~~~~~~~~~~~~~

context: ``worker``

Whether to delete emails after processing.

.. _binary_dependencies:

Binary Dependencies
######################

Papermerge uses a number of open source 3rd parties for various purposes. One
of the most obvious example is tesseract - used to :ref:`OCR <ocr>` documents (extract text
from binary image file). Another, less obvious example, is pdfinfo utility
provided by poppler-utils package: pdfinfo is used to count number of pages in
pdf document. Configurations listed below allow you to override path to
specific dependency.


``BINARY_OCR``
~~~~~~~~~~~~~~~~

context: ``worker``

Full path to tesseract binary/executable file. Tesseract is used for :ref:`OCR <ocr>` operations - extracting of text from binary image files (jpeg, png, tiff).
Default value is::

  BINARY_OCR = "/usr/bin/tesseract"


``BINARY_FILE``
~~~~~~~~~~~~~~~~~

context: ``main app, worker``

File utility used to find out mime type of given file.
Default value is::

  BINARY_FILE = "/usr/bin/file"

``BINARY_CONVERT``
~~~~~~~~~~~~~~~~~~~

context: ``main app, worker``

Convert utility is provided by ImageMagick package.
It is used for resizing images.
Default value is::

  BINARY_CONVERT = "/usr/bin/convert"


``BINARY_PDFTOPPM``
~~~~~~~~~~~~~~~~~~~~~

context: ``main app, worker``

Provided by Poppler Utils.
Used to extract images from PDF file.
Default value is::

  BINARY_PDFTOPPM = "/usr/bin/pdftoppm"

``BINARY_PDFINFO``
~~~~~~~~~~~~~~~~~~~~

context: ``main app, worker``

Provided by Poppler Utils.
Used to get page count in PDF file. Default value is::

  BINARY_PDFINFO = "/usr/bin/pdfinfo"


``BINARY_PDFTK``
~~~~~~~~~~~~~~~~~~

context: ``main app, worker``

Provided by pdftk package (on Ubuntu 20.04 LTS).
Used to reorder, cut/paste, delete pages within PDF document.
Default value is::

  BINARY_PDFTK = "/usr/bin/pdftk"

