FROM ubuntu:19.10

LABEL maintainer="Papermerge Project https://github.com/ciur/papermerge"

RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-venv \
    poppler-utils \
    imagemagick \
    build-essential \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-deu \
    tesseract-ocr-eng && \
    rm -rf /var/lib/apt/lists/*
