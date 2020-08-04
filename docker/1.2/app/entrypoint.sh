#!/bin/bash

# run migrations
cd /opt/papermerge
python3 manage.py migrate
# create superuser
cat create_user.py | python3 manage.py shell

/usr/sbin/cron

exec "$@"