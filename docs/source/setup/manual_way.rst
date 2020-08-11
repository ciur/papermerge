Manual Way
************
### Quick install
Its simplicity makes SQLite extremely useful for development. It speeds up the setup of the development environment.
To start Papermerge for test or development from zero - I need to clone repo, create virtualenv, run migrations and Done!


If I follow this document and still have troubles, I can open an
`issue on GitHub: <https://github.com/ciur/papermerge/issues>`_ so I can fill in the gaps.

1. Within the extracted directory copy ``papermerge.conf.py.example`` to ``/etc/``::

    $ cp papermerge.conf.py.example /etc/papermerge.conf.py
    $ chmod 640 /etc/papermerge.conf.py
    
1. Look at the config-file with your favorite text editor. Leave default settings or adjust to your needs:
    
    * ``DBDIR``: SQLite database storage location
    * ``MEDIA_DIR``: your documents storage location
    * ``STATIC_DIR``: this is where all static files will be collected by ``collectstatic`` command
    * ``IMPORTER_DIR``: Papermerge is looking for new files here

1. Create and Activate python virtual environment with::

    $ python3 -m venv .venv
    $ source .venv/bin/activate

1. Install necessary dependencies::

    $ pip install -r requirements/base.txt

1. Initialize SQLite database with::

    $ ./manage.py migrate

1. Collect static files for webserver with::

    $ ./manage.py collectstatic

6. Create the SuperUser for Papermerge::

    $ ./manage.py createsuperuser

7. Start the webserver with this command to have it reachable from other computers::

    $ ./manage.py runserver 0.0.0.0:8000

If no specific IP or PORT is given (./manage.py runserver), the webserver is only reachable on 127.0.0.1:8000 also known as http://localhost:8000/. 
It should look like in the screenshot below. Use the login credentials that you created in #6 to access Papermerge.

    .. figure:: ../img/login.png

You are almost there, but there is no worker running yet.

8. In a separate shell, change to the project's directory, activate venv and start the worker script with::

    $ ./manage.py worker

9. Now put a JPEG, PNG or TIFF file into the IMPORTER_DIR.
10. Wait a few minutes for Papermerge to run OCR.
   Preview of the documents uploaded:

    .. figure:: ../img/uploaded_docs.png

11. Now you should be able to select text in OCRed document!

.. figure:: ../img/select_text.png

   Now you should be able to select text.

## Start Papermerge at boot

### With a bash script (not tested)
Call the script with a cron-job or within /etc/rc.local and /etc/rc0.d
```
#!/bin/bash
# Start Papermerge at boot

# Wait for boot to complete
sleep 5

# Switch to working directory
cd /home/  user  /papermerge

# Activate v-environment and then run 
source /home/user/folder/bin/activate
manage.py runserver 0.0.0.0:8000&
manage.py worker&
```

### With Systemd (not tested)
create the file in your home directory: nano ~/.config/systemd/user/papermerge.service
```
[Unit]
Description=Start Papermerge at boot

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/  user  /papermerge
ExecStart=source .venv/bin/activate manage.py runserver 0.0.0.0:8000& manage.py worker&

[Install]
WantedBy=default.target
```

Testing and activation:
```
systemctl --user daemon-reload
systemctl --user stop papermerge
systemctl --user start papermerge
systemctl --user restart papermerge
systemctl --user enable papermerge   enable and start the systemd user service:
```
Trouble shooting: https://askubuntu.com/a/1215193
