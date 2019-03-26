FROM python:3.6-alpine3.7

ENV PYTHONUNBUFFERED=0

RUN apk add --no-cache --virtual build-essentials  gcc g++ make sqlite

RUN mkdir /hellworld

WORKDIR /hellworld

ADD . /hellworld

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD python manage.py runserver 0.0.0.0:8000
