workers = 2
errorlog = "{{PROJ_ROOT_DIR}}/var/logs/mysite.gunicorn.error"
accesslog = "{{PROJ_ROOT_DIR}}/var/logs/mysite.gunicorn.access"
loglevel = "debug"

bind = ["127.0.0.1:9001"]
