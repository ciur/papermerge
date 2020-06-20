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

    $ ./manage runserver <IP>:<PORT>

If no specific IP or port is given, the default is 127.0.0.1:8000 also known as http://localhost:8000/. 
At this step, must be able to access login screen and it should look like in
screenshot below. You can login with the user/pass you created in #6.

    .. figure:: ../img/login.png

Also, you can upload some document and see their preview.

    .. figure:: ../img/uploaded_docs.png

But because there is no worker running yet, documents are basically plain images.

8. In a separate window, change to the project's root directory again, but this time, you should start the worker script with ./manage.py worker.

9. Scan something or put a file into the IMPORTER_DIR.
10. Wait a few minutes
11. Now you should be able to select text in OCRed document!


.. figure:: ../img/select_text.png

   Now you should be able to select text
