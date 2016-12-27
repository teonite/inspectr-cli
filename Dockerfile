FROM node:6
MAINTAINER Jacek Chmielewski "jchmielewski@teonite.com"

# https://github.com/npm/npm/issues/9863
RUN cd $(npm root -g)/npm \
 && npm install fs-extra \
 && sed -i -e s/graceful-fs/fs-extra/ -e s/fs\.rename/fs.move/ ./lib/utils/rename.js

RUN apt-get update && apt-get install --assume-yes \
    locales \
    python3 \
    python3-pip

RUN echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN rm /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python
RUN pip3 install --upgrade setuptools

ADD . /inspectr

RUN cd /inspectr/docker && npm install
ENV PATH $PATH:/inspectr/docker/node_modules/.bin/
RUN cd /inspectr && pip3 install -r requirements.pip
RUN cd /inspectr/docker && pip3 install -r reporter-requirements.pip

RUN cd /inspectr && python3 setup.py install

WORKDIR /code
CMD ["inspectr"]
