Migrations, Updates, Backups
=============================


Migrating From 1.2.x -> 1.3.0
##############################

Version 1.2.x runs only with postgresql database.
Version 1.3.0 runs by default with SQLite, but can be configured to run with any database.

In case you upgraded from 1.2 to 1.3 and you want to continue to use PostgreSQL as database you need to consider one more important thing - absolete triggers. In such case you need to manually drop 2 PostgreSQL triggers::

	DROP TRIGGER IF EXISTS tsvector_update_core_page ON core_page

	DROP TRIGGER IF EXISTS tsvector_update_core_basetreenode ON core_page

Obvisouly you need to run usual django migrations as well::

	./manage.py migrate

Migration From 1.3.x -> 1.4.0
##############################

Users you need to run only usual django migrations::

	./manage.py migrate

In case you upgraded from 1.2 directly to 1.4 - then latest version provides a management script to drop triggers for you (in case you opted to continue to use PostgreSQL)::

    ./manage.py drop_triggers

.. note::

	Papermerge docker images created by docker-compose will run drop_triggers management script for you

