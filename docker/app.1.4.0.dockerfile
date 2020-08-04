FROM ubuntu:20.04

LABEL maintainer="Eugen Ciur <eugen@papermerge.com>"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y \
                    build-essential \
                    python3 \
                    python3-pip \
                    python3-venv \
                    virtualenv \
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
 && mkdir -p /opt/media /opt/broker/queue && mkdir /opt/server

RUN groupadd -g 1001 www
RUN useradd -g www -s /bin/bash --uid 1001 -d /opt/app www


# ensures our console output looks familiar and is not buffered by Docker
ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE config.settings.production
ENV PATH=/opt/app/:/opt/app/.local/bin:$PATH

WORKDIR /opt
RUN git clone https://github.com/ciur/papermerge -q --depth 1 /opt/app

RUN chown -R www:www /opt/

USER 1001

WORKDIR /opt/app

ENV VIRTUAL_ENV=/opt/app/.venv
RUN virtualenv $VIRTUAL_ENV -p /usr/bin/python3.8

ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip3 install -r requirements/base.txt --no-cache-dir
RUN pip3 install -r requirements/production.txt --no-cache-dir

COPY app/config/django.production.py /opt/app/config/settings/production.py
COPY app/config/papermerge.config.py /opt/app/papermerge.conf.py


COPY app/entrypoint.sh /opt/entrypoint.sh
COPY app/create_user.py /opt/app/create_user.py



ENTRYPOINT ["/opt/entrypoint.sh"]
