.. _osspecific:

OS Specific Packages
======================

Ubuntu Bionic 18.04 (LTS)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Install required ubuntu packages::

    sudo apt-get update
    sudo apt-get install python3 python3-pip python3-venv \
        poppler-utils \
        imagemagick \
        build-essential \
        tesseract-ocr \
        tesseract-ocr-eng \
        tesseract-ocr-fra \
        tesseract-ocr-deu \
        tesseract-ocr-ron \
        tesseract-ocr-rus \
        tesseract-ocr-spa \
        tesseract-ocr-tur


Every language has its own tesseract-ocr-<code> package. You will have to install tesseract language
package for each language you want to OCR.


Ubuntu Focal 20.04 (LTS)
~~~~~~~~~~~~~~~~~~~~~~~~~

Packages naming (and installation method) did not change from Ubuntu Bionic.


In order to check what language packs are installed, use command::

    $ tesseract --list-langs
    
    List of available languages (5):
    deu
    eng
    fra
    osd
    spa

