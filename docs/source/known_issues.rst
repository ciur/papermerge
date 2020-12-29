Known Issues
================

A list of known problems which won't be fixed.


Case sensitive search for unicode text with SQLite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using SQLite database `unicode strings lookup is always case sensive.
<https://docs.djangoproject.com/en/3.1/ref/databases/#substring-matching-and-case-sensitivity>`_
See `an example of lookup using russian language.
<https://github.com/ciur/papermerge/issues/149>`_ Problem was initially
reported for Bulgarian language.

Warning about missing Tesseract in papermerge_app docker container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you use docker-compose file provided by papermerge repository, you will notice
following error in **papermerge_app docker container**::

    WARNINGS:
    |papermerge_app|: Papermerge can't find tesseract. Without it, OCR of the documents is impossible.
    |papermerge_app|:  HINT: Either it's not in your PATH or it's not installed.

This is very misleading, but it is correct **and has no any impact on papermerge**
operation.

.. note::

    Above mentioned error is safe to ignore only (and only) when it runs in
    main app container i.e. in ``papermerge_app``). Exactly same warning inside
    ``papermerge_worker`` will be an error an application won't function as
    expected.

Explanation:

the OCR is performed by the worker (papermerge_worker docker container) and
thus is installed only on the worker. However, for simplicity sake both worker
and app (papermerge_app and papermerge_worker) use same code. From application
code point of view they are 95% identical and use exactly same methods for
reading configurations.

However:

* for worker - tesseract is mandatory
* for main app - tesseract is optional

as long as that "missing tesseract" comes from papermerge_app docker container
- you can just ignore it.

Current setup (even though little confusing) is very practical. The
practicality of it is that worker and app many times run on same machine, from
same folder and use same configuration file - e.g. in development mode - in
such cases, issuing that warning reminds developers to install
tesseract.

Slow increase in CPU usage over time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In case you use default broker and message queue (which is filesystem based) over time
your CPU usave will increase. Filesystem based message queue is not suitable for production.
You redis to avoid this issue. Learn in :ref:`broker configuration <broker_config>` part how to configure redis.