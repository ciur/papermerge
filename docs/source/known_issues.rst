Known Issues
================

A list of known problems which won't be fixed.


Case sensitive search for unicode text with SQLite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using SQLite database `unicode strings lookup is always case sensive. <https://docs.djangoproject.com/en/3.1/ref/databases/#substring-matching-and-case-sensitivity>`_
See `an example of lookup using russian language. <https://github.com/ciur/papermerge/issues/149>`_
Problem was initially reported for Bulgarian language.