#!/bin/bash

export DJANGO_SETTINGS_MODULE=config.settings.stage
/usr/bin/python3 /opt/papermerge/manage.py txt2db  >> /var/log/cron.log 2>&1 