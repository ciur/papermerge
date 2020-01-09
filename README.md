What it is?
===========

Papermerge is a document management system primarily designed for archiving
and retrieving your digital documents.

This project is a django application i.e. backend part of the whole papermerge
software. If you want to use it's via web browser i.e. with front-end user interface you will need to clone [Papermerge Frontend](https://github.com/ciur/papermerge-js)


Requirements
-------------

    python >= 3.8
    django >= 3.0
    PostgreSQL >= 11.0

Start Application in Development Environment 
---------------------------------------------

To be able to run it in development you will need:
    
    * python >= 3.8
    * nginx >= 1.16.1 
    * PostgreSQL >= 12.1

Although it is django project - it does not use django's builtin web server.


Create and activate python virtual environment
    
    * python -m venv .venv
    * source ./.venv/bin/activate

Install dependencies:

    * pip install -r requirements.txt

Create config/settings/development.py settings (use dev.py as example).
config.settings.development is default DJANGO_SETTINGS_MODULE value.
By config/settings/development.py is ignored by git.

In config/settings/development.py define following variables:

    * STATIC_ROOT
    * DATABASES

STATIC_ROOT is a pathlib.Path(...) instance of path pointing to
where papermerge-js assets are located. Example from my local environment:
    
        STATIC_ROOT = Path('/home/eugen/ciur/papermerge-js/static/')

where /home/eugen/ciur/papermerge-js is a local clone of [papermerge-js](https://github.com/ciur/papermerge-js)



