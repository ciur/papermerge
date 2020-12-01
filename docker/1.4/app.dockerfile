FROM ubuntu:20.04

LABEL maintainer="Eugen Ciur <eugen@papermerge.com>"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y \
                    build-essential \
                    vim \
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
                    locales \
 && rm -rf /var/lib/apt/lists/* \
 && pip3 install --upgrade pip

RUN groupadd -g 1002 www
RUN useradd -g www -s /bin/bash --uid 1001 -d /opt/app www


# ensures our console output looks familiar and is not buffered by Docker
ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE config.settings.production
ENV PATH=/opt/app/:/opt/app/.local/bin:$PATH
RUN echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8


RUN git clone https://github.com/ciur/papermerge  --branch v1.5.3 -q --depth 1 /opt/app

RUN mkdir -p /opt/media

# For broker queue. Change ownership
# so that mounted volume won't make it root-owned
RUN mkdir /opt/app/queue
RUN chown www:www /opt/app/queue

COPY config/app.production.py /opt/app/config/settings/production.py
COPY config/papermerge.config.py /opt/app/papermerge.conf.py
COPY app.startup.sh /opt/app/startup.sh
RUN chmod +x /opt/app/startup.sh
COPY config/create_user.py /opt/app/create_user.py


RUN chown -R www:www /opt/

WORKDIR /opt/app
USER www

ENV VIRTUAL_ENV=/opt/app/.venv
RUN virtualenv $VIRTUAL_ENV -p /usr/bin/python3.8

ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=config.settings.production

RUN pip3 install -r requirements/base.txt --no-cache-dir
RUN pip3 install -r requirements/production.txt --no-cache-dir
RUN pip3 install -r requirements/extra/pg.txt --no-cache-dir

CMD ["/opt/app/startup.sh"]