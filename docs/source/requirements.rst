Requirements
============

Papermerge depends on following software:

* `Python <https://www.python.org/>`_ >= 3.8.0
* `Tesseract <https://github.com/tesseract-ocr/tesseract>`_ - because of OCR
* `Imagemagick <https://imagemagick.org/script/index.php>`_ - Image operations
* `Poppler <https://poppler.freedesktop.org/>`_ - PDF operations
* `PostgreSQL <https://www.postgresql.org/>`_ - because of Full Text Search

Python
#######

Papermerge is a Python 3 application.

Imagemagick
###########

Papermerge uses Imagemagick to convert between images format

Poppler
#########

More exactly poppler utils are used. For exampple pdfinfo command line
utility is used to find out number of page in PDF document.

Tesseract
#########

If you never heard of `Tesseract software
<https://en.wikipedia.org/wiki/Tesseract_(software)>`_ - it is google's open
source `Optical Character Recognition
<https://en.wikipedia.org/wiki/Optical_character_recognition>`_ software.  It
extracts text from images. It works fantastically well for wide range of
languages.

Database
#########

One of Papermerge's core philosophies is "Find Any Document". PostgreSQL
database comes with Full Text Search Support (FTS) out of the box.

With FTS - full text search - you can search documents in similar way people
are used to search web pages in google (bing, yandex, duckduckgo) search
engine - you just type some words - and search result will display only
documents with those words sorted by their relevancy.
