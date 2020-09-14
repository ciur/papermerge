.. _utilities:

Utilities
==========

Utilities are command line tool used to complement various aspects of Papermerge user interface.


.. _backup_command:

Backup
##########

Command to run::
	
	./manage.py backup <location> [--user <username>] [--list]

Backups/Exports all documents. With ``--user <username>`` option will perform **per user** backup.
If you want to list all users in Papermerge use ``--list`` option::

    $ ./manage.py backup --list
    id      username        email
    ----------------------------------
    1       john


.. _restore_command:

Restore
##########

Restores documents from backup tarball. Command to run::

	./manage.py restore <tar-file> [--user <username>]

If backup archive was created with ``--user`` option then you need to use
``--user`` flag to restoration was well (otherwise ``restore`` command will
complain with an error). Restore command takes as mandatory argument tarball
(.tar archive) file created by ``./manage.py backup`` command.

When restoring from system-wide backup (i.e. without ``--user`` option) please make sure
that Papermerge is freshly installed i.e. there are no other user accounts in Papermerge database and that :ref:`media_dir` folder is empty.

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
