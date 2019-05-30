FROM        python:3.6.8-alpine3.7

ARG         PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR     /usr/src/app

RUN         apk add --no-cache --virtual .build-deps \
                build-base \
                openssl-dev \
                libffi-dev \
                zlib-dev \
                libjpeg-turbo-dev \
                libwebp-dev \
                openjpeg-dev \
                tiff-dev \
                linux-headers \
                pcre-dev \
                git \
                curl && \
            # Install pip
            curl -sSL https://bootstrap.pypa.io/get-pip.py | python

COPY        . .
RUN         PIP_NO_BINARY="python-rapidjson" CPPFLAGS="-DRAPIDJSON_SSE42=1" CFLAGS="-msse4.2" pip install -vvvv -r ./requirements.txt && \
            # Whitelist removal
            find /usr/src/app -type f -name "*.pyc" -delete && \
            find /usr/src/app -type f -name "*.pyo" -delete && \
            find /usr/src/app -type d -name "__pycache__" -delete && \
            find /usr/local -type f -name "*.pyc" -delete && \
            find /usr/local -type f -name "*.pyo" -delete && \
            find /usr/local -type d -name "__pycache__" -delete && \
            find /usr/local -type d -name "tests" -exec rm -rf '{}' +
