.. _server_configurations:

Server Configurations
**********************

The default is to use Django’s development server provided by ``./manage.py runserver``
command, as that’s easy and does the job well enough on a home network.
However it is heavily discouraged to use it for more than that.

If you want to do things right you should use a real webserver capable of
handling more than one thread. You will also have to let the webserver serve
the static files (CSS, JavaScript) from the directory configured in
:ref:`static_dir`. The default static files directory is ``static``.

For that you need to activate your virtual environment and collect the static
files with the command::

    $ ./manage.py collectstatic


Nginx + Gunicorn
~~~~~~~~~~~~~~~~~

Step 1 - Gunicorn
###################


Step 2 - Systemd Service for Gunicorn
#######################################


Step 3 - Systemd Service for Worker
#######################################


Step 4 - Nginx
################


Nginx + Uwsgi
~~~~~~~~~~~~~~

Step 1 - Uwsgi
################


Step 2 - Systemd Service for Uwsgi
#######################################


Step 3 - Systemd Service for Worker
#######################################


Step 4 - Nginx
################



Apache
~~~~~~~~



Apache Express
~~~~~~~~~~~~~~~
