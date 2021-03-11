#!/bin/bash

./manage.py makemigrations
./manage.py migrate
cat create_user.py | python3 manage.py shell
./manage.py check
python manage.py worker
