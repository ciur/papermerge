.. _dev_lang_support:

Language Support
=================

Starting with version 1.3.0 (which is now in development) Papermerge can OCR
any language. By default, it is shipped with a preset of :ref:`21 languages
<languages>`. Basically, as of version 1.3.0, developers don't need to change
application's code to have additional languages support.


Language Codes
***************

Language codes are specified in 3 ways:

    * tesseract way
    * django way
    * postgresql way

Tesseract
----------

In tesseract languages are specified using `ISO 639-2/T codes <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_.

To list all installed languages, use command::

    $ tesseract --list-langs

Output example::

    List of available languages (4):
    deu
    eng
    osd
    spa

Django
-------

Work in progress


Postgresql
-----------

Work in progress