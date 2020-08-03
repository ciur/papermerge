FROM ubuntu:20.04

LABEL maintainer="Eugen Ciur <eugen@papermerge.com>"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y \
                    build-essential \
                    python3 \
                    python3-pip \
                    python3-venv \
                    poppler-utils \
                    git \
                    imagemagick \
                    pdftk-java \
                    apache2 \
                    apache2-dev \
                    tesseract-ocr \
                    tesseract-ocr-deu \
                    tesseract-ocr-eng \
                    tesseract-ocr-fra \
                    tesseract-ocr-spa \
 && rm -rf /var/lib/apt/lists/* \
 && pip3 install --upgrade pip \
 && mkdir -p /opt/media /opt/broker/queue

# ensures our console output looks familiar and is not buffered by Docker
ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE config.settings.production

WORKDIR /opt
RUN git clone https://github.com/ciur/papermerge -q --depth 1 /opt/papermerge
 
WORKDIR /opt/papermerge
RUN pip3 install -r requirements/base.txt
RUN pip3 install -r requirements/production.txt

COPY app/config/django.production.py /opt/papermerge/config/settings/production.py
COPY app/config/papermerge.config.py /opt/papermerge/papermerge.conf.py


COPY app/entrypoint.sh /opt/entrypoint.sh
COPY app/create_user.py /opt/papermerge/create_user.py

ENTRYPOINT ["/opt/entrypoint.sh"]
