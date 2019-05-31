FROM        python:3.6.8-alpine3.7

ARG         PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR     /usr/src/app

RUN         apk add --no-cache --virtual .build-deps \
                build-base \
                openssl-dev \
                libffi-dev

COPY        . .
RUN         PIP_NO_BINARY="python-rapidjson" CPPFLAGS="-DRAPIDJSON_SSE42=1" CFLAGS="-msse4.2" pip install -vvvv -r ./requirements.txt
