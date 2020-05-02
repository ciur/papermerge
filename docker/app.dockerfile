FROM ubuntu:19.10

LABEL maintainer="Eugen Ciur <eugen@papermerge.com>"

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

ENV DJANGO_SETTINGS_MODULE config.settings.stage

WORKDIR /opt
RUN git clone https://github.com/ciur/papermerge -q --depth 1 --branch v1.2.1 /opt/papermerge \
 && git clone https://github.com/ciur/papermerge-js --depth 1 --branch v1.2.0 /opt/papermerge-js

WORKDIR /opt/papermerge
RUN pip3 install -r requirements.freeze

COPY app/settings.py /opt/papermerge/config/settings/stage.py

COPY app/entrypoint.sh /opt/entrypoint.sh
COPY app/create_user.py /opt/papermerge/create_user.py

COPY etc/* /etc/system/systemd/

ENTRYPOINT ["/opt/entrypoint.sh"]
