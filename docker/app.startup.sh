#!/bin/bash

if [ ! -f "/opt/etc/production.py" ]; then
    cp /opt/defaults/production.py /opt/etc/production.py
fi

if [ ! -f "/opt/etc/papermerge.conf.py" ]; then
    cp /opt/defaults/papermerge.conf.py /opt/etc/papermerge.conf.py
fi

ln -sf /opt/etc/production.py /opt/app/config/settings/production.py
ln -sf /opt/etc/papermerge.conf.py /opt/app/papermerge.conf.py

./manage.py makemigrations
./manage.py migrate
cat create_user.py | python3 manage.py shell

./manage.py collectstatic --no-input
./manage.py check

mod_wsgi-express start-server \
    --server-root /opt/app/\
    --url-alias /static /opt/static  \
    --url-alias /media /opt/media \
    --port 8000 --user www --group www \
    --log-to-terminal \
    --limit-request-body 20971520 \
    config/wsgi.py

# --limit-request-body 20971520 options is to limit
# max upload size to 20 MB
