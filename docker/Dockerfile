FROM ubuntu:16.04

MAINTAINER Zafer Durkut, <mailto:durkutzafer@gmail.com>


ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y python3 \
    python3-dev \
    vim \
    python3-pip \
    libmysqlclient-dev \
    gdal-bin \
    python3-gdal \
    libgdal-dev \
    python-gdal \
    locales \
    wget \
    net-tools \
    unzip

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

RUN pip3 install -r requirements.txt

RUN ln -sf /usr/bin/python3 /usr/bin/python
