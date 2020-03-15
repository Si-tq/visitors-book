FROM python:3.7.4-alpine3.9

ENV PYTHONUNBUFFERED 1

ENV PG_VERSION 11.7-r0

COPY requirements.txt /tmp/

RUN apk add --no-cache python3-dev libstdc++ && \
    apk add --no-cache g++ && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN set -ex \
		&& apk add --no-cache \
			 postgresql-dev=$PG_VERSION \
		&& apk add --no-cache \
			 gettext \
			 bash \
			 libmagic \
			 postgresql-client=$PG_VERSION \
		&& apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
		        openssl \
				libressl2.7-libcrypto \
		&& pip install --upgrade pip \
		&& pip install --upgrade setuptools \
		&& pip install --no-cache-dir -r /tmp/requirements.txt \
&& rm -rf /tmp/requirements.txt

RUN mkdir /src

WORKDIR /src

COPY . /src

EXPOSE 8000