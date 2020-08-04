#!/bin/bash

source .venv/bin/activate
export DJANGO_SETTINGS_MODULE=config.settings.production

# run migrations
cd /opt/app
python3 manage.py migrate
# create superuser
cat create_user.py | python3 manage.py shell

python3 manage.py collectstatic --no-input

python3 manage.py runmodwsgi --working-directory . \
        --host 0.0.0.0 \
        --port 8000 \
        --user www \
        --group www \
        --url-alias /static /opt/static \
        --url-alias /media /opt/media \
        --setup-only \
        --server-root /opt/server \
        --access-log

/opt/server/apachectl start        

exec "$@"