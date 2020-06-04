Manual Way
************

.. warning::

    Starting with version 1.3.0 (which is now in development), manual installation will be simplified a lot. The installation process be as easy as 1. pip install papermerge 2. ./manage.py migrate 3. ./manage.py createsuperuser 4. ./manage.py runserver
    Also, in version 1.3.0 the PostgreSQL part will be optional i.e. you will be able to use Papermerge with other databases we well e.g. sqlite.


Papermerge has two parts:
 
    * :ref:`Web application <design>`
    * :ref:`Worker <worker>` - which is used for OCR operation

With this installation method both parts will run on the same computer.
This installation method is suitable for developers. In this method
no configuration is automated, so it is a **perfect method if you want to
understand the mechanics** of the project.

If you follow along in this document and still have trouble, please open an
`issue on GitHub: <https://github.com/ciur/papermerge/issues>`_ so I can fill in
the gaps.

.. _packages-and-db:

Package Dependencies
======================

In this setup, Web App and Workers run on the same machine. 

Install :ref:`os specific packages for webapp + worker <osspecific1>` 

Check that Postgres version 11 is is up and running::

    sudo systemctl status postgresql@11-main.service

Create new role for postgres database::

    sudo -u postgres createuser --interactive

When asked *Shall the new role be allowed to create databases?* please answer yes 
(when running tests, django creates a temporary database) 

Create new database owned by previously created user::

    sudo -u postgres createdb -O <user-created-in-prev-step> <dbname>

Set a password for user::
    
    sudo -u postgres psql
    ALTER USER <username> WITH PASSWORD '<password>';


Web App
========

Once we have prepared database, tesseract and other dependencies, let's start
with paperpermerge itself.

Clone main papermerge project::

    git clone --branch v1.2.2 https://github.com/ciur/papermerge papermerge-proj

Clone papermerge-js project (this is the frontend part)::

    git clone --branch v1.2.2 https://github.com/ciur/papermerge-js

Create python's virtual environment .env::

    cd papermerge-proj
    python3 -m venv .venv

Activate python's virtual environment::    
    
    source .venv/bin/activate

Install required python packages (now you are in papermerge-proj directory)::
    
    # while in <papermerge-proj> folder
    pip install -r requirements.txt


Rename file *config/settings/development.example.py* to *config/settings/development.py*.
This file is default for DJANGO_SETTINGS_MODULE and it is included in .gitignore.

Adjust following settings in *config/settings/development.py*:

* :ref:`DATABASES <databases>` -  name, username and password of database you created in PostgreSQL
* :ref:`STATICFILES_DIRS <staticfilesdirs>` - include path to <absolute_path_to_papermerge_js_clone>/static
* MEDIA_ROOT - absolute path to media folder
* :ref:`STORAGE_ROOT`- absolute path to same media root, but with a "local:/" prefix

.. note::

    1. Make sure that ``data_folder_in`` and ``data_folder_out`` point to the same location.
    2. Make sure that folder pointed by ``data_folder_in`` and ``data_folder_out`` exists.

Then, as in any django based project, run migrations, create super user and run build in webserver::

      cd <papermerge-proj>
     ./manage.py migrate
     ./manage.py createsuperuser
     ./manage.py runserver


At this point, you should be able to see (styled) login page.  You should be
able as well to login with administrative user you created before with
``./manage.py createsuperuser`` command.

At this step, must be able to access login screen and it should look like in
screenshot below.

    .. figure:: ../img/login.png

Also, you can upload some document and see their preview.

    .. figure:: ../img/uploaded_docs.png

But because there is no worker configured yet, documents are basically plain images.
Let's configure worker!

Worker
=======

Let's add a worker *on the same machine* with Web Application we configured above.
We will use the same python's virtual environment as for Web Application.

.. note::
    
    Workers are the ones who depend on (and use) tesseract not Web App.

Clone repo and install (in same python's virtual environment as Web App)
required packages::

    git clone https://github.com/ciur/papermerge-worker
    cd papermerge-worker
    pip install -r requirements.txt

Create a file <papermerge-worker>/config.py with following configuration::

    worker_concurrency = 1
    broker_url = "filesystem://"
    broker_transport_options = {
        'data_folder_in': '/home/vagrant/papermerge-proj/run/broker/data_in',
        'data_folder_out': '/home/vagrant/papermerge-proj/run/broker/data_in',
    }
    worker_hijack_root_logger = True
    task_default_exchange = 'papermerge'
    task_ignore_result = False
    result_expires = 86400
    result_backend = 'rpc://'
    include = 'pmworker.tasks'
    accept_content = ['pickle', 'json']
    s3_storage = 's3:/<not_used>'
    local_storage = "local:/home/vagrant/papermerge-proj/run/media/"

.. important::

    Folder pointed by ``data_folder_in`` and ``data_folder_out`` must exists and be
    the same one as in configuration for Web Application.


Now, while in <papermerge-worker> folder, run command::

    CELERY_CONFIG_MODULE=config  celery worker -A pmworker.celery -Q papermerge -l info

At this stage, if you keep both built in webserver (./manage.py runserver
command above) and worker running in foreground and upload a couple of PDF
documents, and obvisouly give worker few minutes time to OCR the document,
document becomes more than an image - you can now select text in it!


.. figure:: ../img/select_text.png

   Now you should be able to select text



Recurring Commands
====================

At this point, if you will try to search a document - nothing will show up in search
results. It is because, workers OCR a document and place results into a .txt file, thus
extracted text is not yet in database.

A special Papermerge command ``txt2db`` will read .txt files and insert them
in associated documents' (documents' pages) database entries.

Afterwards another command ``update_fts`` will prepare a special a database column
with correct information about document (more precicely - page).

Run commands manually::

    cd <papermerge-proj>
    ./manage.py txt2db
    ./manage.py update_fts


.. note::

    In manual setup (i.e. without any Papermerge's background services running),
    if you want a document to be available for search, you need to run ``./manage.py txt2db``
    and ``./manage.py update_fts`` commands everytime after document is OCRed.


