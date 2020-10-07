.. figure:: img/logo.png

Papermerge DMS
===============

I have nothing against paper. Paper is a brilliant invention of humanity. But in the
21st century I find it more appropriate for paper-based documents to be
digitized (scanned). Once scanned, appropriate software can be used to find any
document in a fraction of a second, just by typing a few keywords.


Papermerge is a document management system designed to work with scanned
documents. As well as :ref:`OCR <ocr>` with full text search, it provides the look and feel of
major modern file browsers, **with tags** and hierarchical structure for files and folders,
so that you can organize your documents in a similar way to Dropbox (via web)
or Google Drive (but with tags and other cool features).

What It Does
============

 * It :ref:`OCRs <ocrs>` your documents
 * Provides you nice user interface to easly browse your documents
 * Augments your documents with :doc:`metadata <metadata>`
 * Helps you instantly find your documents:
    
    * based on extracted text
    * based on :doc:`metadata <metadata>`
    * based on :doc:`tags <tags>`

 * Helps you fix scanned documents issues


What It Doesn't Do
==================
 
 * It does **not** take control of your documents. Documents are **stored on filesystem** in a simple and intuitive manner so that you can take snapshot of your data at any time.
 * It does **not** stay in your way when you make decisions about your data. 

.. toctree::
   :maxdepth: 4
   
   intro
   requirements
   setup/index
   consumption
   languages
   file_formats
   rest_api
   backup_restore
   page_management
   metadata
   tags
   automation
   user_management
   access_permissions
   utilities
   updates
   settings
   known_issues
   translators_guide/index
   developers_guide/index
   changelog
   glossary



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
