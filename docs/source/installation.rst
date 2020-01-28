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

Set a password for user::
    
    sudo -u postgres psql
    ALTER USER <username> WITH PASSWORD '<password>';

Clone main papermerge project::

    git clone https://github.com/ciur/papermerge papermerge-proj

Clone papermerge-js project (this is the frontend part)::

    git clone https://github.com/ciur/papermerge-js

Create python's virtual environment .env::

    cd papermerge-proj
    python3 -m venv .venv

Activate python's virtual environment::    
    
    source .venv/bin/activate

Install required python packages (now you are in papermerge-proj directory)::
    
    # while in <papermerge-proj> folder
    pip install -r requirements.txt

**********************
Configure Papermerge
**********************

Rename file *config/settings/development.example.py* to *config/settings/development.py*.
This file is default for DJANGO_SETTINGS_MODULE and it is included in .gitignore.

Adjust following settings in *config/settings/development.py*::

* DATABASES['NAME'] - name of database you created in PostgreSQL
* DATABASE['USER'] - name of user for PostgreSQL database
* STATIC_ROOT - this settings must point to the <full_dir_path_of_papermerge_js_clone>/static
* MEDIA_ROOT - absolute path to media folder
* STORAGE_ROOT - absolute path to same media root, but with a "local:/" prefix

Then, as in any django based project, run migrations, create super user and run build in webserver::

     ./manage.py migrate
     ./manage.py createsuperuser
     ./manage.py runserver


