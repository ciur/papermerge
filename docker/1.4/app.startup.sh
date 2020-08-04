#!/bin/bash

./manage.py makemigrations
./manage.py migrate
# in version 1.2 there were triggers defined
# Since version 1.4, triggers are not used anymore
# drop triggers
./manage.py drop_triggers
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
