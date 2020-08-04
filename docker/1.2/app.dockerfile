FROM ubuntu:20.04

LABEL maintainer="Eugen Ciur <eugen@papermerge.com>"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y \
                    python3 \
                    python3-pip \
                    python3-venv \
                    poppler-utils \
                    git \
                    imagemagick \
                    build-essential \
                    tesseract-ocr \
                    tesseract-ocr-deu \
                    tesseract-ocr-eng \
                    cron \
 && rm -rf /var/lib/apt/lists/* \
 && pip3 install --upgrade pip \
 && mkdir -p /opt/media /opt/broker/queue

# ensures our console output looks familiar and is not buffered by Docker
ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE config.settings.stage

WORKDIR /opt
RUN git clone https://github.com/ciur/papermerge -q --depth 1 --branch v1.2.3 /opt/papermerge \
 && git clone https://github.com/ciur/papermerge-js --depth 1 --branch v1.2.2 /opt/papermerge-js

WORKDIR /opt/papermerge
RUN pip3 install -r requirements.freeze

COPY app/settings.py /opt/papermerge/config/settings/stage.py

COPY app/entrypoint.sh /opt/entrypoint.sh
COPY app/create_user.py /opt/papermerge/create_user.py

COPY app/crontab /etc/cron.d/papermerge
COPY app/txt2db.sh /opt/txt2db.sh
RUN chmod 0744 /opt/txt2db.sh
COPY app/update_fts.sh /opt/update_fts.sh
RUN chmod 0744 /opt/update_fts.sh
COPY app/hello.sh /opt/hello.sh
RUN chmod 0744 /opt/hello.sh

RUN chmod 0644 /etc/cron.d/papermerge
RUN crontab /etc/cron.d/papermerge
RUN touch /var/log/cron.log
CMD cron

ENTRYPOINT ["/opt/entrypoint.sh"]
