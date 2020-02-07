Docker
**********

1. Install `Docker <https://www.docker.com/>`_
2. Install `docker-compose <https://docs.docker.com/compose/install/>`_
3. Clone Papermerge Repository::

    git clone https://github.com/ciur/papermerge papermerge-proj

4. Run docker compose command::

    cd papermerge-proj/docker
    docker-compose up --build -d

This will create and start the necessary containers. 
Papermerge Web Service is available at **http://localhost:8000**
For initial sign in use::
    
    URL: http://localhost:8000
    username: admin
    password: admin

