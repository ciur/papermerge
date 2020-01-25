Requirements
============

Papermerge depends on following software:

* `Python <https://www.python.org/>`_ >= 3.8.0
* `Tesseract <https://github.com/tesseract-ocr/tesseract>`_ - because of OCR
* `Imagemagick <https://imagemagick.org/script/index.php>`_ - Image operations
* `Poppler <https://poppler.freedesktop.org/>`_ - PDF operations
* `PostgreSQL <https://www.postgresql.org/>`_ - because of Full Text Search

If you never heard of `Tesseract software
<https://en.wikipedia.org/wiki/Tesseract_(software)>`_ - it is google's open
source `Optical Character Recognition
<https://en.wikipedia.org/wiki/Optical_character_recognition>`_ software.  It
extracts text from images. It works fantastically well for wide range of
languages.

You may wonder why isn't it database agnostic? Or maybe why for installtion ease 
