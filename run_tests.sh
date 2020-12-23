#!/bin/bash

export DJANGO_SETTINGS_MODULE=config.settings.test

./manage.py test \
    papermerge/test/ \
    $@
