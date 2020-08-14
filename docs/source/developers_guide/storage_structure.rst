Storage Structure
==================

The primary configuration which determines where uploaded documents
are stored is :ref:`media_dir`. It must be a directory on your local filesystem.

Inside :ref:`media_dir` there two important folders:

    1. docs - stores original (raw, unaltered) documents
    2. results - stores useful information extracted from documents

.. note::

    If you didn't upload any document yet, then :ref:`media_dir` directory will be empty (*docs* and *results* will be missing as well).

    When you upload a document, :ref:`media_dir`/*docs* direcory is 
    created.

Original documents are stored under following format:

    * :ref:`media_dir`/docs/user_<id>/document_<id>/<filename>



