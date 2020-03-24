.. _dev_lang_support:

Language Support
*******************

By default, papermerge is hardcoded to work with documents in only two languages -
German and English. Theoretically it can support more than 100 languages.
However, I, as developer and user of this software, included in papermerge only what was
usefull for me (German and English).

You can contribute to this project by adding support (and testing it) for you own language.
It is extremely rewarding experience, because:

    * it is fun
    * you will learn a lot
    * you will create something useful for you and others


What is Language Support?
==========================

There are two parts to consider:

    * User Interface language (text like username, Log out)
    * Document Content (actual content of your documents)



User Interface Language
========================

User Interface language is text you user sees and interacts with. Say labels
for username in German will be Benutzername, or text for Log out in German is
Abmelden. To localize user interface (UI) in your own language you need be
familiar with  `Django way
<https://docs.djangoproject.com/en/3.0/topics/i18n/>`_. It is because main web
application is Django project. 

Contributing to the project in this sense means basically creating/updating file papermerge/<langcode>/LC_MESSAGES/django.po file.


Document Content Language
==========================

Every document upload to papermerge will be OCRed by `tesseract <https://github.com/tesseract-ocr/tesseract>`_ command line utility. Tesseract command requires -l <lang> argument - to indicate the language of the document. This is the heart of *document language support*. Have a look a worker's shortcuts module `extract_hocr and extract_txt <https://github.com/ciur/papermerge-worker/blob/master/pmworker/shortcuts.py#L42>`_ functions. Both functions built tesseract command with language as first argument.


To check what languages you have installed for tesseract, use command::

    $ tesseract --list-langs

In my case, it lists `deu` and `eng` - which are codes for German and English languages.

OCRing of the documents (tesseract -l deu path/to/doc) happens on worker side.
I explained this because it is important to know, but for adding language
support - you **don't need to change anything in the worker**, because worker only takes orders and blindly executes them.

The entry point, for the worker part is task module with it's `ocr_page function <https://github.com/ciur/papermerge-worker/blob/378477d3f6769bea49e1145e8fc4a6b799fa464b/pmworker/tasks.py#L79>`_. Again, no need to change anything here, I mention this only because it is important to know.

First thing you need to have a look into and change is `dynamic_preferences_module <https://github.com/ciur/papermerge/blob/026e7fbce4cbd1e02a8d55e1619a1626849187bd/papermerge/core/dynamic_preferences_registry.py#L42>`_ where configuration for to language is defined. 

You will need to add a new choice in OcrLanguage class. The code for the new language **must** match language code listed by ``tesseract --list-langs``. This change will add a new entry in UI and will allow user to choose new language for the document.

But the tricky part is doing the change on database level. The thing is papermerge makes use of `PostgreSQL full text search feature <https://www.postgresql.org/docs/current/textsearch.html>`_,  which means it needs to store an updated version of tsvector type column. 
How to create and search tsvector type columns is described in `postgres documentation <https://www.postgresql.org/docs/current/textsearch-tables.html>`_.

Every time page.text column is changed a database level trigger is fired to updated language specific tsvector column. 
Triggers for this job are defined in `papermerge/core/pgsql/01_triggers.sql <https://github.com/ciur/papermerge/blob/master/papermerge/core/pgsql/01_triggers.sql>`_ file.

Another important language related sql file is `papermerge/core/pgsql/03_update_lang_cols.sql <https://github.com/ciur/papermerge/blob/master/papermerge/core/pgsql/03_update_lang_cols.sql>`_. This sql code is executed periodically by `papermerge/core/management/commands/update_fts.py <https://github.com/ciur/papermerge/blob/master/papermerge/core/management/commands/update_fts.py>`_ command. It is responsable for moving document page.text to page.text_deu or text to text_eng.

Both page.text_eng and page.text_deu are tsvector type columns with preset weight 'C'.
