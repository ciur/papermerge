.. _utilities:

Utilities
==========

Utilities are command line tool used to complement various aspects of Papermerge user interface.


.. _backup_command:

Backup
##########

Backups/Exports all docs

.. _restore_command:

Restore
##########

Restores docs


.. _importer_command:

Importer
#########

Imports documents from email attachments and from local folder.

Command to run::

	$ ./manage.py importer <local_directory>

.. _worker_command:

Worker
#######

Most important task of the built-in worker is to perform documents' OCR. Also, if :ref:`settings_email` settings are defined (at least email host and email user) - will import periodically (once in 30 seconds), documents from specified email account. Similarly if :ref:`importer_dir` is defined - every 30 seconds - will fetch documents from specified directory.

Command to run::

	$ ./manage.py worker
