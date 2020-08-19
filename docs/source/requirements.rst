Requirements
============

You need a Linux machine or Unix-like setup that has the following software installed:

* `Python <https://www.python.org/>`_ >= 3.7
* `Django <https://www.djangoproject.com/>`_ >= 3.0
* `Tesseract <https://github.com/tesseract-ocr/tesseract>`_ - because of :ref:`OCR <ocr>`
* `Imagemagick <https://imagemagick.org/script/index.php>`_ - Image operations
* `Poppler <https://poppler.freedesktop.org/>`_ - PDF operations

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


In addition to the above, there are a number of Python requirements, all of which are listed in a file called ``requirements/base.txt`` in the project root directory.
