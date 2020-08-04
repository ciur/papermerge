#!/bin/bash


export PATH=/opt/app/.venv/bin/:$PATH

mod_wsgi-express start-server \
	--server-root  /opt/app/ \
    --url-alias /static /app/static \
    --url-alias /media /app/media \
    --port 8000 --user www --group www \
    --log-to-terminal \
    config/wsgi.py

exec "$@"