{{notice}}

workers = 4
errorlog = "{{proj_root}}/run/log/gunicorn.error"
accesslog = "{{proj_root}}/run/log/gunicorn.access"
loglevel = "debug"

bind = ["127.0.0.1:9001"]
