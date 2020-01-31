.. _osspecific:

OS Specific Packages
======================

Here are given instructions on how to install operating system specific packages. There
are three cases.
    
    1. Both web app and workers are on same machine
    2. Web app machine
    3. Worker machine

.. _osspecific1
1. Web App + Workers Machine
------------------------------

Ubuntu Bionic 18.04 (LTS)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Install required ubuntu packages::

    sudo apt-get update
    sudo apt-get install python3 python3-pip python3-venv \
        poppler-utils \
        imagemagick \
        build-essential \
        poppler-utils \
        tesseract-ocr \
        tesseract-ocr-deu \
        tesseract-ocr-eng

Notice that for tesseract :ref:`only english and german <languages>` (Deutsch)
language packages are needed.

Ubuntu Bionic 18.04 comes with postgres 10 package. Papermerge on the other hand
requires at least version 11 of Postgres. 

Install Postgres version 11::

    # add the repository
    sudo tee /etc/apt/sources.list.d/pgdg.list <<END
    deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main
    END

    # get the signing key and import it
    wget https://www.postgresql.org/media/keys/ACCC4CF8.asc
    sudo apt-key add ACCC4CF8.asc

    # fetch the metadata from the new repo
    sudo apt-get update

.. _osspecific2
2. Web App Machine
--------------------


.. _osspecific3
3. Worker Machine
--------------------
