FROM postgres:11.6


ADD ./init_db.sh /docker-entrypoint-initdb.d/