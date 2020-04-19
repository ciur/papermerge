.. _languages:

Languages Support
===================

 .. DANGER::
   This feature is still work in progress. It will be available since version
   1.3.0. Up until version 1.2.0 (which is now current stable) only support for
   German and English languages was included.

Theorethically all languages supported by tesseract (over 130) can be used.
By default, Papermerge comes with a preset of following 21 languages:

    * Arabic
    * Danish
    * Dutch
    * English
    * Finnish
    * French
    * German
    * Hungarian
    * Indonesian
    * Irish
    * Italian
    * Lithuanian
    * Nepali
    * Norwegian
    * Portuguese
    * Romanian
    * Russian
    * Spanish
    * Swedish
    * Tamil
    * Turkish

.. note::

    How those 21 languages were chosen ? Well, by default, PostgreSQL 12.0 database comes with
    a preset of 21 dictionaries. You can see installed dictionaries in psql with `\\dFd` command.

If you want to use other languages, you need to do 3 things:

    * include them in :ref:`MG_OCR_LANGUAGES` dictionary
    * install tesseract data for new languages (on worker machines)
    * install postgres dictionary for new languages
