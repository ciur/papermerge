Manual Way
************

If you follow this document and still have troubles, please open an
`issue on GitHub: <https://github.com/ciur/papermerge/issues>`_ so I can fill in
the gaps.

1. Within extracted directory copy ``papermerge.conf.py.example`` to ``/etc/``::

    $ cp papermerge.conf.py.example /etc/papermerge.conf.py
    $ chmod 640 /etc/papermerge.conf.py
    
1a. Look at the config-file with your favorite text editor. Leave default settings or adjust to your needs:
    
    * ``DB_DIR``: SQLite database storage location
    * ``MEDIA_DIR``: your documents storage location
    * ``STATIC_DIR``: this is where all static files will be collected by ``collectstatic`` command
    * ``IMPORTER_DIR``: Papermerge is looking for new files here

2. Create and Activate python virtual environment with::

    $ python3 -m venv .venv
    $ source .venv/bin/activate

3. Install necessary dependencies::

    $ pip install -r requirements/base.txt

4. Initialize SQLite database with::

    $ ./manage.py migrate

5. Collect static files for webserver with::

    $ ./manage.py collectstatic

6. Create a user for Papermerge instance::

    $ ./manage.py createsuperuser

7. Start webserver with::

    $ ./manage.py runserver <IP>:<PORT>

If no specific IP or PORT is given, the default is 127.0.0.1:8000 also known as http://localhost:8000/. 
It should look like in the screenshot below. Use the login credentials that you created in #6 to access Papermerge.

    .. figure:: ../img/login.png

You are almost there, but there is no worker running yet.

8. In a separate window, change to the project's root directory again, but this time, you should start the worker script with ./manage.py worker.

9. Now put a JPEG, PNG or TIFF file into the IMPORTER_DIR.
10. Wait a few minutes for Papermerge to run OCR.
   Preview of the documents uploaded:

    .. figure:: ../img/uploaded_docs.png

11. Now you should be able to select text in OCRed document!


.. figure:: ../img/select_text.png

   Now you should be able to select text
