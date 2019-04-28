FROM python:3.6-alpine3.7

ENV PYTHONUNBUFFERED=0

ENV DJANGO_SETTINGS_MODULE=hellworld.settings.production
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_STORAGE_BUCKET_NAME=$AWS_STORAGE_BUCKET_NAME

RUN apk add --no-cache --virtual build-deps curl gcc g++ make postgresql-dev bash

RUN mkdir /hellworld

RUN mkdir /task_inputs

WORKDIR /hellworld

ADD . /hellworld

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements_production.txt
