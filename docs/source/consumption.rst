Consumption
=============

Once you’ve got Papermerge set up, you need to start feeding documents into it. Currently, there are four options: upload directly via web user interface, the importer directory, IMAP (email), and the REST API.

Uploading document via web interface won't be explained here as it is very obvious. Uploading via REST API along with how to register a token is explained in :ref:`REST API <rest_api>`. Here we will focus on importing from a local directory and importing documents from an email account (imap).

The Importer Directory
~~~~~~~~~~~~~~~~~~~~~~~

You point Papermerge to a specific directory on your local system and
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

IMAP (Email)
~~~~~~~~~~~~~

Importing documents from an email account is very similar to importing documents from  a local directory. The same rules applies for email as well:

    1. Email importing settings must be defined on the worker side.
    2. Imported documents will end up in the first superuser's inbox.

The following are :ref:`email importing settings <settings_email>` you need to configure:

* ``IMPORT_MAIL_HOST``
* ``IMPORT_MAIL_USER``
* ``IMPORT_MAIL_PASS``
* ``IMPORT_MAIL_SECRET``

host, user and password are those of the IMAP server host (email server host), your IMAP
user and password respectively. The *secret* thingy is there to make sure that
Papermerge will read only emails it is supposed to. Any email not containing
that secret word will be ignored.

.. note::

    Only the first email attachment will be imported - the rest of them will be ignored. After importing the document from your email attachment, the email message will **not** be deleted.



