Consumption
=============

Once you’ve got Papermerge setup, you need to start feeding documents into it. Currently, there are four options: upload directly via web user interface, the importer directory, IMAP (email), and REST API.

Uploading document via web interface won't be explained here as it is very obvious. Uploading via REST API along with how to register a tocken is explaned in :ref:`REST API <rest_api>`. Here we will focus on importing from local directory and importing documents from email account (imap).

The Importer Directory
~~~~~~~~~~~~~~~~~~~~~~~

You point Papermerge to a specific directory on your local system and
:ref:`worker <worker_command>` script will import all documents from that
directory. Getting stuff into this directory is up to you. If you’re running
Paperless on your local computer, you might just want to drag and drop files
there.  Imported documents will land in your Inbox folder.

The configuration settings you are looking for is :ref:`IMPORTER_DIR <importer_dir>`. It points to directory where all documents will be imported from. Example::

    IMPORTER_DIR = "/mnt/media/importer_dir"

Directory pointed by IMPORTER_DIR must be readable by Papermerge application.

.. note::

    Notice that ``IMPORTER_DIR`` must be defined on worker side. For single deployments worker and main app will share same ``papermerge.conf.py`` configuration file, thus all configurations will be in same configuration file. In case of distributed deployment - or even in case when main app and worker run within different docker images - this distinction becomes important. ``IMPORTER_DIR`` should be defined in ``papermerge.conf.py`` of the host (or docker image) where worker runs.

All imported documents will land in superuser's Inbox.

.. note::

    Papermerge is multi-user system. Very first system user is called superuser. Papermerge must have at least one superuser.
    Regardless how many users there are in Papermerge DMS, imported documents will always end up in first superuser's inbox.

IMAP (Email)
~~~~~~~~~~~~~

Importing documents from email account is very similar to importing documents from local directory. Same rules applies for email as well:

    1. Email importing settings must be defined on the worker side.
    2. Imported documents will end up in first superuser's inbox.

Following are :ref:`email importing settings <settings_email>` you need to configure:

* ``IMPORT_MAIL_HOST``
* ``IMPORT_MAIL_USER``
* ``IMPORT_MAIL_PASS``
* ``IMPORT_MAIL_SECRET``

host, user and password are IMAP server host (email server host), your IMAP
user and password respectively. The *secret* thingy is there to make sure that
Papermerge will read only emails it is supposed to. Any email not containing
that secret word will be ignored.

.. note::

    Only one (first one) email attachment will be imported - rest of them will be ignored. After importing document from your email attachment email message will **not** be deleted.



