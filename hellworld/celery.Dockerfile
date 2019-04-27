FROM python:3.6-alpine3.7

ENV PYTHONUNBUFFERED=0

RUN apk add --no-cache --virtual build-deps curl gcc g++ make postgresql-dev bash

RUN mkdir /hellworld

WORKDIR /hellworld

ADD . /hellworld

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements_production.txt
