#!/bin/bash

export DJANGO_SETTINGS_MODULE=config.settings.stage
/usr/bin/python3 /opt/papermerge/manage.py update_fts  >> /var/log/cron.log 2>&