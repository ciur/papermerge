Installation
=============

Papermerge has two parts:
 
    * `Web App <https://github.com/ciur/papermerge>`_
    * `Worker <https://github.com/ciur/papermerge-worker>`_ - which is used for OCR operation

Depending on your needs both Worker and Web App can run on same machine  or
you can setup a fully distributed application with as many workers (each on
separate machine) you need.

I developed, tested and deployed only on Linux machines, just because I am linux user.
Theorethically installation should be easy to adopt for MacOS machines.  


Development Environment
############################

In this setup, Web App and Workers run on single machine. 

***************************
Ubuntu Bionic 18.04 (LTS)
***************************

Install required ubuntu packages::

    sudo apt-get update
    sudo apt-get install python3 python3-pip python3-venv \
        poppler-utils \
        imagemagick \
        build-essential \
        poppler-utils \
        tesseract-ocr \
        tesseract-ocr-deu \
        tesseract-ocr-eng

Notice that for tesseract :ref:`only english and german <languages>` (Deutsch) language packages are needed.

