FROM        python:3.7.3-alpine3.8

ARG         PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR     /usr/src/app

RUN         apk add --no-cache --virtual .build-deps \
                build-base \
                openssl-dev \
                libffi-dev

COPY        . .
RUN         PIP_NO_BINARY="python-rapidjson" CPPFLAGS="-DRAPIDJSON_SSE42=1" CFLAGS="-msse4.2" pip install -vvvv -r ./requirements.txt
