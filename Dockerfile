FROM mhart/alpine-node:6
MAINTAINER Jacek Chmielewski "jchmielewski@teonite.com"

RUN apk add --no-cache \
    python3 \
    python3-dev\
    build-base && \
    python3 -m ensurepip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip && \
    rm -rf /usr/lib/python*/ensurepip

ADD . /inspectr

RUN cd /inspectr/docker && npm install -g
RUN cd /inspectr && pip3 install -r requirements.pip
RUN cd /inspectr/docker && pip3 install -r reporter-requirements.pip

RUN cd /inspectr && python setup.py install

VOLUME /code /root/.inspectr_connector.json

WORKDIR /code
CMD ["inspectr"]
