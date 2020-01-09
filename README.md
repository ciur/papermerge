What it is?
===========

Papermerge is a document management system primarily designed for archiving
and retrieving your digital documents.


Requirements
============

    python >= 3.8
    django >= 3.0
    PostgreSQL >= 11.0

Development
===========

1. Create and activate python virtual environment
    
    * python -m venv .venv
    * source ./.venv/bin/activate

2. Install dependencies:

    * pip install -r requirements.txt

3. Create config/settings/development.py settings (use dev.py as example).
 config.settings.development is default DJANGO_SETTINGS_MODULE value.

4. In config/settings/development.py define following variables:

    * STATIC_ROOT
    * DATABASES