FROM ubuntu:18.04
FROM python:3.6

ARG secret_key

RUN apt-get update && apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev net-tools

RUN pip install -U pip setuptools
RUN pip install uwsgi

COPY ./webroms /opt/webroms
RUN mkdir -p /var/log/uwsgi/

WORKDIR /opt/webroms

RUN pip install -r requirements.txt

ENV SECRET_KEY !86=*ez09+b6@nm03$ml7x4b02n5j)e43t^28vh50av_1a+-dl

ENV DJANGO_SETTINGS_MODULE config.settings.dev

COPY ./docker/dev/web/uwsgi.ini /opt/webroms/uwsgi.ini
COPY ./docker/dev/web/domigrate.sh /opt/webroms
COPY ./docker/dev/web/createsuperuser.sh /opt/webroms

ENTRYPOINT ["uwsgi", "--ini", "uwsgi.ini"]
