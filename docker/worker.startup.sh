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
./manage.py check
python manage.py worker
