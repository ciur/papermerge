#!/bin/bash

# run migrations
cd /opt/app
python3 manage.py migrate
# create superuser
cat create_user.py | python3 manage.py shell

exec "$@"