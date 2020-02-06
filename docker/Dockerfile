FROM ubuntu:19.10

LABEL maintainer="Eugen Ciur <eugen@papermerge.com>"

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

RUN mkdir -p /opt/
RUN cd /opt && \
    git clone https://github.com/ciur/papermerge && \
    git clone https://github.com/ciur/papermerge-worker && \
    git clone https://github.com/ciur/papermerge-js

RUN cd /opt/papermerge && \
    python3 -m venv .venv && \
    . /opt/papermerge/.venv/bin/activate && \
    pip install -r requirements.freeze

COPY settings.py /opt/papermerge/config/settings/stage.py

