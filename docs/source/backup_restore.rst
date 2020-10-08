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

    Backup does not save users' passwords unless option
    ``--include-user-password`` is specified. For papermerge system-wide
    backups created without ``--include-user-password`` option after restoring
    the backup, system administrator need to set superuser password with
    ``./manage changepassword`` command. Superuser in turn, will need to set
    passwords for other Papermerge accounts.

Detailed Version
~~~~~~~~~~~~~~~~~~~

System-wide or Per User?
#########################

There are at two different backup strategies:

    * System-wide - will backup/restore all documents of all users in Papermerge instance
    * Per User - will backup/restore all documents **only for specific user**

You can opt for *per user backup strategy* with ``--user <username>`` switch.

..  important::

    If backup file was created with ``--user <username>`` switch, **it must** be restored with same
    ``--user <username>``. If you forget to add ``--user`` option, ``./manage.py restore`` command will
    complain with an error.

.. important::

    Term **system-wide** here refers to Papermerge system - which is same as
    saying **for all users in Papermerge database**. Don't confuse usage of
    term system here with operating system, or Linux system.

Per user backup strategy is very convenient when there is only one user in
Papermerge. This strategy will backup all documents and preserve their folder
structure. No user information will be stored in backup file.

System-wide (for all accounts in Papermerge) strategy will backup data per
each user in Papermerge instance. Along with documents, it will save
information like username, email and if that user is superuser or not. Note
however that users's passwords won't be saved unless you explicitely ask for
it with ``--include-user-password`` option.

Backup
########

To create a **backup of all documents** currently found your in Papermerge instance, just run::

    ./manage.py backup

This will create a file `backup_<current-datetime>.tar` in same folder where `manage.py` file is located.

You can provide a file name as well::

    ./manage.py backup papermerge.tar

Notice tar extension. You can provide any file name (or path to a file) but keep in mind that backup command creates a tar archive for you.

Finally you can provide as argument an existing directory::

    ./manage.py backup /data/backups/papermerge/

In example above, file named
`/data/backups/papermerge/backup_<current-datetime>.tar` will be created.

For full reference see :ref:`backup <backup_command>` and :ref:`restore
<restore_command>` commands in utils documentation.

Restore
#########

.. note::
    Before restoring a system-wide backup, please make sure that
    :ref:`media_dir` is empty and you don't have any user account created
    i.e. your Papermerge system was just freshly installed.

To restore documents from tar archive, use following command::

    ./manage.py restore <path-to-tar-file>

As main argument for `restore` command use provide path to tar archive.

.. warning::
    
    Keep in mind that `restore` command expects tar archive - **not zipped**
    tar archive. In case your backup solution pipeline compressed tar archive
    provided by `backup` command - you will need to first uncompress it
    manually, and then provide it as argument to restore command.

Example of usage::

    ./manage.py restore papermerge_13_07_2020.tar

Because system-wide **backups don't store users passwords**, you will need to set superuser
password anew::

    $ ./manage changepassword <superuser-username>
