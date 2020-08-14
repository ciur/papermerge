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

Things start to be very interesting when it comes to second directory of :ref:`media_dir` - *results* directory. As its name suggests, *results* directory is where processed results are stored. Important information stored in *results* folder is following:

    1. Document's OCRed text - stored per page (as .txt).
    2. Document's OCRed information stored in hOCR format (as .hocr).
    3. Associated images of each document's page.

Here is an example of how *results* directory look like for upload document with id=2 corresponding to user with id=1:


.. figure:: img/storage_structure/02_results_dir.svg

Notice that point 1 in illustration above shows (arrow marked with red circle
with number 1 on it) document_2 directory from *results* corresponds to
document_2 directory from *docs*.

As you can see in red square (red A) - Papermerge works on page level i.e. it
extract information for each page separately. In yellow square (marked with
yellow letter E) you see that Papermege extracted text information and stores
it in .txt files for each page. Thus, document in picture above, has 3 pages.
Text from page_<xyz>.txt files will be copied into database and then later
indexed. This allows users to perform searches per document's page.