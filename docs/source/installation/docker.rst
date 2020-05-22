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

