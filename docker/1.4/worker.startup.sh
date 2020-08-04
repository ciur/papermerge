#!/bin/bash

./manage.py migrate
# # create superuser
cat create_user.py | python3 manage.py shell
# 
./manage.py check
# 
python manage.py worker

# RUN ./manage.py migrate
# # create superuser
# RUN cat create_user.py | python3 manage.py shell
# 
# RUN ./manage.py check
# 
# CMD ["python", "manage.py", "worker"]