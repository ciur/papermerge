Docker
**********

With this method you will need ``git``, ``docker`` and ``docker-compose`` installed.


1. Install `Docker <https://www.docker.com/>`_
2. Install `docker-compose <https://docs.docker.com/compose/install/>`_
3. Clone Papermerge Repository::

    git clone https://github.com/ciur/papermerge papermerge-proj

4. Run docker compose command (which will pull images from `DockerHub <https://hub.docker.com/r/eugenci/papermerge>`_)::

    cd papermerge-proj/docker
    docker-compose up -d

This will pull and start the necessary containers. If you wish, you can use ``docker-compose -f docker-compose-dev.yml up --build -d`` command instead to build local images.

Check if services are up and running::

    docker-compose ps

Papermerge Web Service is available at ``http://localhost:8000``
For initial sign in use::
    
    URL: http://localhost:8000
    username: admin
    password: admin

You can check logs of each service with::

    docker-compose logs worker
    docker-compose logs app
    docker-compose logs db


Main App, Worker or Both?
===========================

The command ``docker-compose up`` starts three containers:

* main app (exact container name is papermerge_app)
* worker (exact container name is papermerge_worker)
* postgres_db

By default, both ``main app`` and ``worker`` container will have their own
copy of ``papermerge.conf.py``. In case you want to change/adjust ``papermerge.conf.py``
you need to take into account for whom that configuration applies.
All :ref:`settings` have in their description a field *context* with one of three values:

    1. main app
    2. worker
    3. main app, worker

In first and second cases configuration needs to be changed only on main app or
worker respectively. When *context* field states ``main app, worker`` - it
means that respective configuration variable must be changed on both main app
**AND** worker to function properly. 


Configuration Changes in Docker Container
===========================================
 
Here is how you can apply configuration changes on the running docker containers.
First, make sure docker containers are up and running::

    $docker ps

    CONTAINER ID        IMAGE                             COMMAND                  CREATED              STATUS              PORTS                    NAMES
    3018d5fc00cf        eugenci/papermerge-worker:1.4.3   "/opt/app/startup.sh"    4 seconds ago        Up 3 seconds                                 papermerge_worker
    3e554df78f5d        eugenci/papermerge:1.4.3          "/opt/app/startup.sh"    About a minute ago   Up 2 seconds        0.0.0.0:8000->8000/tcp   papermerge_app
    ba160197ff8c        postgres:12.3                     "docker-entrypoint.s…"   22 hours ago         Up 3 seconds        5432/tcp                 postgres_db

Then, *login* to running docker of e.g. worker container. In example above CONTAINER ID of the worker is *3018d5fc00cf*::

    $ docker exec -it 3018d5fc00cf /bin/bash
    www@3018d5fc00cf:~$ whoami
    www
    www@3018d5fc00cf:~$ pwd
    /opt/app
    www@3018d5fc00cf:~$ cat papermerge.conf.py

    DBUSER = "***"
    DBPASS = "***"
    DBHOST = "***"
    DBNAME = "***"

    MEDIA_DIR = "/opt/media"
    STATIC_DIR = "/opt/static"
    MEDIA_URL = "/media/"
    STATIC_URL = "/static/"

    OCR_DEFAULT_LANGUAGE = "deu"

    OCR_LANGUAGES = {
        "deu": "Deutsch",
        "spa": "Spanish",
    }

If you want to add *English* as additional language and make it default :ref:`ocr` language. I need to change ``OCR_LANGUAGES`` and ``OCR_DEFAULT_LANGUAGE`` as follows::

    OCR_DEFAULT_LANGUAGE = "eng"

    OCR_LANGUAGES = {
        "eng": "English",
        "deu": "Deutsch",
        "spa": "Spanish",
    }

Note that you **don't need to install** tesseract's English language pack as it is already part of the worker image::

    www@3018d5fc00cf:~$ tesseract --list-langs

    List of available languages (5):
    deu
    eng
    fra
    osd
    spa


In both :ref:`ocr_languages` and :ref:`ocr_default_language` settings, there is a line mentioning "context: main app, worker" - it means that you need to change these settings in **both worker and main app**. So, in next step, change ``OCR_LANGUAGES`` and ``OCR_DEFAULT_LANGUAGE`` in main app as well::

    $ docker ps
    CONTAINER ID        IMAGE                             COMMAND                  CREATED             STATUS              PORTS                    NAMES
    3018d5fc00cf        eugenci/papermerge-worker:1.4.3   "/opt/app/startup.sh"    16 minutes ago      Up 16 minutes                                papermerge_worker
    3e554df78f5d        eugenci/papermerge:1.4.3          "/opt/app/startup.sh"    18 minutes ago      Up 16 minutes       0.0.0.0:8000->8000/tcp   papermerge_app
    ba160197ff8c        postgres:12.3                     "docker-entrypoint.s…"   23 hours ago        Up 16 minutes       5432/tcp                 postgres_db

    $ docker exec -it 3e554df78f5d /bin/bash
    # same changes as for worker container
    # cat papermerge.conf.py
    # etc etc

Restart containers. Restarting containers will preserve changes you made to papermerge.conf.py.