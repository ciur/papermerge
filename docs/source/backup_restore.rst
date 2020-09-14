.. _backup_restore:

Backup/Restore
===============

For your peace of mind, Papermerge provides easy way to backup/export and restore all your documents.
Terms *backup* and *export* (similar for *restore*/*import*) are synonymous so they will be use here interchangeably.


Short Version
~~~~~~~~~~~~~~~~~
    1. To backup all document in Papermerge (for all users)::

        $ ./manage.py backup

    2. To restore given backup::

        $ ./manage.py restore <path-to-tar-file>

.. important::

    Backup **does not save users' passwords**. This means that after restoring the backup, system administrator need to set superuser password with ``./manage changepassword`` command. Superuser in turn, will be to set passwords for other Papermerge users.

Detailed Version
~~~~~~~~~~~~~~~~~~~

Backup
########

To create a **backup of all documents** currently found your in Papermerge instance, just run::

    ./manage.py backup

This will create a file `backup_<current-datetime>.tar` in same folder where `manage.py` file is located.

You can provide a file name as well::

    ./manage.py backup papermerge.tar

Notice tar extension. You can provide any file name (or path to a file) but keep in mind that backup command creates a tar archive for you
.
Finally you can provide as argument an existing directory::

    ./manage.py backup /data/backups/papermerge/

In example above, file named `/data/backups/papermerge/backup_<current-datetime>.tar` will be created.

For full reference see :ref:`backup <backup_command>` and :ref:`restore <restore_command>` commands in utils documentation.

Restore
#########

To restore documents from tar archive, use following command::

    ./manage.py restore <path-to-tar-file> --user <username>

As main argument for `restore` command use provide path to tar archive.

.. warning::
    
    Keep in mind that `restore` command expects tar archive - **not zipped** tar archive. In case your backup solution pipeline compressed tar archive provided by `backup` command - you will need to first uncompress it manually, and then provide it as argument to restore command.

User argument expects a *username* - not an id.
Example of usage::

    ./manage.py restore papermerge_13_07_2020.tar --user admin

