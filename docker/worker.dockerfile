FROM ubuntu:19.10

LABEL maintainer="Eugen Ciur <eugen@papermerge.com>"

ENV DJANGO_SETTINGS_MODULE config.settings.stage

RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-venv \
    poppler-utils \
    git \
    nginx \
    imagemagick \
    build-essential \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-deu \
    tesseract-ocr-eng && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/media
RUN mkdir -p /opt/broker/queue

RUN cd /opt && \
    git clone https://github.com/ciur/papermerge-worker

# ensures our console output looks familiar and is not buffered by Docker 
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
RUN cd /opt/papermerge-worker && \
    pip3 install -r requirements.freeze

COPY worker/config.py /opt/papermerge-worker/config.py
