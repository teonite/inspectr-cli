FROM node:6
MAINTAINER Jacek Chmielewski "jchmielewski@teonite.com"

# https://github.com/npm/npm/issues/9863
RUN cd $(npm root -g)/npm \
 && npm install fs-extra \
 && sed -i -e s/graceful-fs/fs-extra/ -e s/fs\.rename/fs.move/ ./lib/utils/rename.js

RUN apt-get update && apt-get install --assume-yes \
    python3 \
    python3-pip

RUN pip3 install --upgrade setuptools

ADD . /inspectr

RUN cd /inspectr/docker && npm install -g
RUN cd /inspectr && pip3 install -r requirements.pip
RUN cd /inspectr/docker && pip3 install -r reporter-requirements.pip

RUN cd /inspectr && python3 setup.py install

VOLUME /code /root/.inspectr_connector.json

WORKDIR /code
CMD ["inspectr"]
