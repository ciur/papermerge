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

Updating Papermerge is three step operation:

    1. update code (backend i.e. python code)
    2. run database migrations
    3. update/static content (frontend i.e. javascript, css, images)


Step 1 - Update Code
~~~~~~~~~~~~~~~~~~~~~~

First of all you need to update application code. You need to either :ref:`download <download>` the `latest tarball <https://github.com/ciur/papermerge/releases>`_ or checkout directly from repository with following git command::

    $ git checkout -b <latest-stable-release>

For example::

    $ git checkout -b v1.4.2

.. note::

    In case you update via git command, you need to invoke first ``git pull``
    command, which will retrieve latest code changes from github.
    Only after ``git pull`` you can ``git checkout`` to latest version.
    To see all available local versions, use command ``git tag``. Similarly 
    you need to ``git pull`` before ``git tag`` to see latest versions.
    ``git pull`` brings latest changes from github to your local computer.

.. danger::
    
    Never use git **master branch** in production. Master branch contains latest development version of Papermerge - which makes it highly unstable. Stable versions are tagged. For example ``v1.4.2`` is the latest tagged version of ``stable/1.4.x`` branch.

With latest code available, you need to activate your python's current virtual environment::

    source .venv/bin/activate

And then run::

    pip3 install -r requirements/base.txt

This will upgrade all 3rd party modules dependencies.


Step 2 - Run Database Migrations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now it is time to apply changes to the database.
With your python virtual environment active, run following command::

    $ ./manage.py migrate

The above command will run so called database migrations. This means that
database schema (i.e. database used by Papermerge instance) will be updated to
match latest python code changes e.g. new column will be added, maybe a column
rename etc.


Step 3 - Update Static Content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Last step is to copy new static content into :ref:`static_dir` folder::

    $ ./manage collectstatic

Above command will take latest version of javascript, css, images i.e. static content and copy it to :ref:`static_dir`.
