#!/bin/bash

./manage.py migrate
# create superuser
cat create_user.py | python3 manage.py shell

./manage.py collectstatic --no-input
./manage.py check

mod_wsgi-express start-server \
    --server-root /opt/app/ \
    --url-alias /static /opt/static  \
    --url-alias /media /opt/media \
    --port 8000 --user www --group www \
    --log-to-terminal \
    config/wsgi.py

#RUN ./manage.py migrate
## create superuser
#RUN cat create_user.py | python3 manage.py shell
#
#RUN ./manage.py collectstatic --no-input
#RUN ./manage.py check
#
#CMD ["mod_wsgi-express", "start-server", \
#     "--server-root",  "/opt/app/", \
#    "--url-alias", "/static", "/opt/static", \
#    "--url-alias", "/media", "/opt/media", \
#    "--port", "8000", "--user", "www", "--group", "www", \
#    "--log-to-terminal", \
#    "config/wsgi.py"]