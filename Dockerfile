FROM mhart/alpine-node:6
MAINTAINER Jacek Chmielewski "jchmielewski@teonite.com"

RUN apk update && apk add --no-cache \
    python3 \
    python3-dev\
    build-base && \
    python3 -m ensurepip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip && \
    rm -rf /usr/lib/python*/ensurepip

ADD . /inspectr

RUN cd /inspectr/docker && npm install -g
RUN pip install --upgrade pip
RUN cd /inspectr && pip install -r requirements.pip
RUN cd /inspectr/docker && pip install -r reporter-requirements.pip

RUN cd /inspectr && python setup.py install

VOLUME /code /root/.inspectr_connector.json

WORKDIR /code
CMD ["inspectr"]
