FROM postgres:11.6


ADD ./db/entrypoint.sh /docker-entrypoint-initdb.d/