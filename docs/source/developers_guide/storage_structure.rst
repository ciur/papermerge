Storage Structure
==================

The primary configuration which determines where uploaded documents
are stored is :ref:`media_dir`. It must be a directory on your local filesystem.

Inside :ref:`media_dir` there two important folders:

    1. docs - stores original (raw, unaltered) documents
    2. results - stores useful information extracted from documents

.. note::

    If you didn't upload any document yet, then :ref:`media_dir` directory will be empty (*docs* and *results* will be missing as well). Even more - :ref:`media_dir` directory itself might not be created yet.

    Both *docs* and *results* directories are created for when you upload first document.

Original documents are stored under following format:

    * :ref:`media_dir`/docs/user_<id>/document_<id>/<filename>

The picture below illustrates show how :ref:`media_dir` (= media) looks like after two .pdf documents were uploaded:

.. figure:: img/storage_structure/01_media_dir.png

