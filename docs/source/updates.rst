Updates and Migrations
======================


Before updating to newer version, it is highly recommended to :ref:`backup
<backup_restore>` your data first. In general it is a good idea to backup your
own data regularly. :ref:`backup_restore` details in great depth about how to
safely store your important data with Papermerge.


.. note::

    If you use Papermerge inside docker container, then updating to newer vesion
    of Papermerge implies just change of tagged image - everything else will
    happen behind the scene.

Following sections describes the process of updating/migration to newer
version of Papermerge. It is addressed to **system administrators** or maintainers
of Papermerge instances.

Updating Papermerge is three fold operation:

    * update code (backend i.e. python code)
    * update/migrate database
    * update/static content (frontend i.e. javascript, css, images)