FROM ubuntu:16.04

MAINTAINER Zafer Durkut, <mailto:durkutzafer@gmail.com>


WORKDIR /app
COPY . /app

ENV LANG=C.UTF-8

RUN set -ex; \
    apt-get install -y python3 \
    python3-dev \
    vim \
    python3-pip \
    libmysqlclient-dev \
    gdal-bin \
    locales \
    wget \
    unzip \
    apt-get update -y; \
    apt-get upgrade -y; \
    apt-get install -y build-essential; \
    apt-get install -y python-dev;\
    apt-get install -y default-libmysqlclient-dev;\
    apt-get install -y python-mysqldb;\
    pip install -U -v setuptools; \
    pip install --no-cache-dir -r requirements.txt; \
    pip install ipdb; \
    apt-get clean; \
    apt-get autoclean; \
    apt-get autoremove; \
    rm -rf /tmp/* /var/tmp/*; \
    rm -rf /var/lib/apt/lists/*; \
    rm -rf /var/cache/apt/archives/*.deb \
        /var/cache/apt/archives/partial/*.deb \
        /var/cache/apt/*.bin; \

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

RUN pip3 install --upgrade pip &&  \
    pip3 install --upgrade setuptools

RUN pip3 install -r requirements.txt

RUN ln -s /usr/bin/python3 /usr/bin/python