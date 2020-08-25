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