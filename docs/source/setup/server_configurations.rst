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

Setting up a web server can sound daunting for folks who don't normally do
that kind of thing. This guide will help you walk through the configuration
for Apache or Nginx on Linux and OSX.

If this all looks too overwhelming for you, we do offer `affordable hosted
solutions <https://papermerge.com/pricing>`_ for folks who want to use
Papermerge but don't know how to run a web server, or don't have time to keep
up with updates.


Apache
~~~~~~~~

The most common setup for Papermerge on a linux server is to use Apache, so if
you're not sure what to pick, Apache might be the best bet, as it's free, easy
to configure, and well documented.

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



Worker
~~~~~~~~
Here is worker.service unit::

    [Unit]
    Description=Papermerge Worker
    After=network.target

    [Service]
    Type=simple
    WorkingDirectory=/opt/papermerge
    ExecStart=/opt/papermerge/.venv/bin/python /opt/papermerge/manage.py worker --pidfile /tmp/worker.pid
    Restart=on-failure

    [Install]
    WantedBy=multi-user.target

.. note::

    Notice that ``ExecStart`` is **absolute path to python interpreter inside
    python virtual environment**. Absolute path to python interpreter inside
    virtual environment is enough information for python to figure out the
    rest of python dependencies from the same virtual environment. Thus, you
    don't need to provide futher information about virtual environment.

Systemd .service may be placed in one of several locations. One options is
to place it in ``/etc/systemd/system`` together with other system level
units. In this case you need root access permissions.

Another option is to place .service file inside ``$HOME/.config/systemd/user/``
In this case you can start/check status/stop systemd unit service with following commands::

    systemctl --user start worker
    systemctl --user status worker
    systemctl --user stop worker

.. note::

    
