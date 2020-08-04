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
                    nginx \
                    imagemagick \
                    build-essential \
                    poppler-utils \
                    tesseract-ocr \
                    tesseract-ocr-deu \
                    tesseract-ocr-eng \
 && rm -rf /var/lib/apt/lists/* \
 && pip3 install --upgrade pip \
 && mkdir -p /opt/media /opt/broker/queue

# ensures our console output looks familiar and is not buffered by Docker
ENV PYTHONUNBUFFERED 1

ENV CELERY_CONFIG_MODULE=config

RUN git clone --depth=1 https://github.com/ciur/papermerge-worker --branch v1.2.0 /opt/papermerge-worker

WORKDIR /opt/papermerge-worker
RUN pip3 install -r requirements.freeze

COPY worker/config.py /opt/papermerge-worker/config.py
COPY worker/logging.yml /opt/papermerge-worker/logging.yml
