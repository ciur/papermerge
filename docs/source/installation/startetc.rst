Startetc 
**********

In this installation method you use a special papermerge command ``startetc``
to generate a bunch of configuration files in ``<papermerge-proj>/run/etc``
folder. Then only with one single command::

    systemctl --user start papermerge

you start a full fledged staging environment with nginx, gunicorn, one worker and recurring commands
running as services on a single machine. I really love this method and I use in my local development
environment.

Package Dependencies
======================

You will need to install :ref:`os specific packages for webapp + worker <osspecific1>` first.
Then make sure that PostreSQL is up and running.
