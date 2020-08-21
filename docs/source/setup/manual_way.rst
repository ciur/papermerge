Manual Way
************

If you follow this document and still have troubles, please open an
`issue on GitHub: <https://github.com/ciur/papermerge/issues>`_ so I can fill in
the gaps.

This guide is split into two parts: short one and very detailed one. 
:ref:`manual_way_short_version` is meant for people who are confortable with development tools
like Python, Django, pip, git or even gcc. In this case I will skip most of details
as they will sound boring for such persons.

:ref:`manual_way_detailed_version` is for people who probably heard of Python - as programming
language - but do not have any experience working with it. Any form of prior
programming (in ruby, perl, java, C/C++) experience will help you to grasp the
concepts quicker.

In both versions of this guide you need to know what is a command line
terminal and how to work with it. In general Papermerge is a Linux/Unix based
software. In this guide I will use Ubuntu 20.04 as example, but this
instructions can be adopted easily for any Linux distribution.

.. _manual_way_short_version:

Short Version
~~~~~~~~~~~~~~~

First :ref:`download` the sorce code.


1. Within extracted directory copy ``papermerge.conf.py.example`` to ``/etc/``::

    $ cp papermerge.conf.py.example /etc/papermerge.conf.py
    $ chmod 640 /etc/papermerge.conf.py
    
1a. Look at the config-file with your favorite text editor. Leave default settings or adjust to your needs:
    
    * ``DBDIR``: SQLite database storage location
    * ``MEDIA_DIR``: your documents storage location
    * ``STATIC_DIR``: this is where all static files will be collected by ``collectstatic`` command
    * ``IMPORTER_DIR``: Papermerge is looking for new files here

2. Create and Activate python virtual environment with::

    $ python3 -m venv .venv
    $ source .venv/bin/activate

3. Install necessary dependencies::

    $ pip install -r requirements/base.txt

4. Initialize SQLite database with::

    $ ./manage.py migrate

5. Collect static files for webserver with::

    $ ./manage.py collectstatic

6. Create a user for Papermerge instance::

    $ ./manage.py createsuperuser

7. Start webserver with::

    $ ./manage.py runserver <IP>:<PORT>

If no specific IP or PORT is given, the default is 127.0.0.1:8000 also known as http://localhost:8000/. 
It should look like in the screenshot below. Use the login credentials that you created in #6 to access Papermerge.

    .. figure:: ../img/login.png

You are almost there, but there is no worker running yet.

8. In a separate window, change to the project's root directory again, but this time, you should start the worker script with ./manage.py worker.

9. Now put a JPEG, PNG or TIFF file into the IMPORTER_DIR.
10. Wait a few minutes for Papermerge to run OCR.
   Preview of the documents uploaded:

    .. figure:: ../img/uploaded_docs.png

11. Now you should be able to select text in OCRed document!


.. figure:: ../img/select_text.png

   Now you should be able to select text

.. _manual_way_detailed_version:

Detailed Version
~~~~~~~~~~~~~~~~~~


Step 1 - Python and Friends
#############################

Papermerge is written in Python. First thing you need to make sure python interpreter is installed.
Ubuntu 20.04 comes with python interpreter already installed. 
However, the command to invoke python interpreter is ``python3``::

    $ python3 --version
    Python 3.8.2


.. note::
    
    Python community now transitions from python2 (which is not maintained
    anymore) to python3. This is why in many Linux distributions you can
    access python interpreter either with ``python`` command or with
    ``python3`` command. 

.. important::
        Make sure your python is at least version 3.7


Although Papermerge is written in python, it uses some *special*
python modules which are compiled from C sources and used in binary form. This
means that you need `gcc compiler <https://gcc.gnu.org/>`_ installed as well.

In Ubuntu 20.04, ``gcc`` is available via ``built-essential`` package::

    sudo apt install build-essential
