#!/bin/bash

./manage.py makemigrations
./manage.py migrate
# in version 1.2 there were triggers defined
# Since version 1.4, triggers are not used anymore
# drop triggers
./manage.py drop_triggers
cat create_user.py | python3 manage.py shell
./manage.py check
python manage.py worker
