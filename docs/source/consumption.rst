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

IMAP (Email)
~~~~~~~~~~~~~




