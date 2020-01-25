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

Notice that for tesseract :ref:`only english and german <languages>` (Deutsch)
language packages are needed.

Install PostgreSQL::

    sudo apt install postgresql postgresql-contrib

This will install PostgreSQL version 10. Check that it is up and running::

    sudo systemctl status postgresql@10-main.service

Create new role for postgres database::

    sudo -u postgres createuser --interactive

When asked *Shall the new role be allowed to create databases?* please answer yes 
(when running tests, django creates a temporary database) 

Create new database owned by previously created user::

    sudo -u postgres createdb -O <user-created-in-prev-step> <dbname>






