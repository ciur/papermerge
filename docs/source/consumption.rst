Consumption
=============

Once you’ve got Papermerge set up, you need to start feeding documents into it. Currently, there are four options: upload directly via web user interface, the importer directory, IMAP (email), and the REST API.

Uploading document via web interface won't be explained here as it is very obvious. Uploading via REST API along with how to register a token is explained in :ref:`REST API <rest_api>`. Here we will focus on importing from a local directory and importing documents from an email account (imap).


.. _importer_directory:

The Importer Directory
~~~~~~~~~~~~~~~~~~~~~~~

You can point Papermerge to a specific directory on your local system and
:ref:`worker <worker_command>` script will import all documents from that
directory. Getting stuff into this directory is up to you. If you’re running
Papermerge on your local computer, you might just want to drag and drop files
there.  Imported documents will land in your Inbox folder.

The configuration setting you are looking for is :ref:`IMPORTER_DIR <importer_dir>`. It points to the directory where all documents will be imported from. Example::

    IMPORTER_DIR = "/mnt/media/importer_dir"

The IMPORTER_DIR directory pointed must be readable by the Papermerge application.

.. note::

    Notice that ``IMPORTER_DIR`` must be defined on the worker side. For single deployments worker and main app will share the same ``papermerge.conf.py`` configuration file, thus all configurations will be in same configuration file. In case of distributed deployment - or even in case when the main app and worker run within different docker images - this distinction becomes important. ``IMPORTER_DIR`` should be defined in ``papermerge.conf.py`` of the host (or docker image) where the worker runs.

All imported documents will land in superuser's Inbox.

.. note::

    Papermerge is a multi-user system. The very first system user is called superuser. Papermerge must have at least one superuser.
    Regardless of how many users there are in Papermerge DMS, imported documents will always end up in first superuser's inbox.

.. _importer_imap:

IMAP (Email)
~~~~~~~~~~~~~

Importing documents from an email account is very similar to importing documents from  a local directory. The following rules apply for email importing:

    1. Email importing settings must be defined on the worker side.
    2. Unless one of the ``IMPORTED_MAIL_BY_*`` is set, imported documents will end up in the first superuser's inbox.
    3. Settings are both global and per-user.

The following are :ref:`email importing settings <settings_email>` you need to configure:

* ``IMPORT_MAIL_HOST``
* ``IMPORT_MAIL_USER``
* ``IMPORT_MAIL_PASS``
* ``IMPORT_MAIL_BY_USER``
* ``IMPORT_MAIL_BY_SECRET``
* ``IMPORT_MAIL_DELETE``

The admin should set ``HOST``, ``USER``, and ``PASS`` to the credentials of the IMAP server to which users will send
emails to have them processed by Papermerge. ``IMPORT_MAIL_BY_USER`` allows user to send emails from their
user-configured email address and have them end up in their inbox if they so choose. ``IMPORT_MAIL_BY_SECRET``
allows user to insert a per-user secret (formatted as ``SECRET{<GENERATED_SECRET>}``) in their emails to have them
put in their own inbox. Finally if ``IMPORT_MAIL_DELETE`` is set then a processed email will be deleted from
the mail account.


