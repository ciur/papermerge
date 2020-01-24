Requirements
============

You need a computer with following software installed:

* `Python <https://www.python.org/>`_ >= 3.8.0
* `Tesseract <https://github.com/tesseract-ocr/tesseract>`_ - because of OCR
* `Imagemagick <https://imagemagick.org/script/index.php>`_ - Image operations
* `Poppler <https://poppler.freedesktop.org/>`_ - PDF operations
* `PostgreSQL <https://www.postgresql.org/>`_ - because of Full Text Search

Papermerge has two parts:
 
    * `Web App <https://github.com/ciur/papermerge>`_
    * `Worker <https://github.com/ciur/papermerge-worker>`_ - which is used for OCR operation

Depending on your needs both Worker and Web App can run on same machine (not
recommened) - or you can setup a fully distributed application with as many
workers (each on separate machine) you need.
