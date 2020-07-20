User Management
================


Users
~~~~~~~~

Papermerge is mult-user system. This means that you can create multiple users.
The most privileged user is called superuser or administrator. In order to use
Papermerge, you need at least one user - superuser.

.. note::

	You can create superuser from command-line using ``./manage.py createsuperuser``
	command.

Only superuser can manage (i.e. create, delete) other users.


Groups
~~~~~~~~

Groups are convinient way to, well, group other users. If for example you want to assign
same permission on a specific folder for multiple users (e.g. For-Accounts folder, must be accessible
only to users from accounting department) - then you need to create group Accountants and add
all accountants to Accountants group.