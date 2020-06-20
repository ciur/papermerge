Manual Way
************

If you follow along in this document and still have trouble, please open an
`issue on GitHub: <https://github.com/ciur/papermerge/issues>`_ so I can fill in
the gaps.

1. Within extracted directory copy ``papermerge.conf.py.example`` to ``/etc/papermerge.conf.py`` and open it in editor. Set values for:
    
    * ``IMPORTER_DIR``: this is local filesystem directory from where your documents will be imported
    * ``DB_DIR``: this is local directory where sqlite database file will be stored
    * ``MEDIA_DIR``: this is where all your document files will be saved
    * ``STATIC_DIR``: this is where all static files will be collected by ``collectstatic`` command

2. Create and activate python virtual environment with::

    $ python -m venv .venv
    $ source .venv/bin/activate

3. Install dependencies in requirements.txt::

    $ pip install -r requirements.txt

4. Initialize SQLite database with::

    $ ./manage.py migrate

5. Collect static files for webserver with::

    $ ./manage.py collectstatic

6. Create user for Papermerge instance::

    $ ./manage.py createsuperuser

7. Start webserver with::

    $ ./manage runserver

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


