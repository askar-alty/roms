FROM ubuntu:18.04
FROM python:3.6

RUN apt-get update && apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev net-tools


RUN pip install -U pip setuptools
RUN pip install uwsgi

COPY ./webroms /opt/webroms
RUN mkdir -p /var/log/uwsgi/

WORKDIR /opt/webroms

RUN pip install -r requirements.txt

ENV NMAP_CONTROL_ADDRESS 172.23.0.1

ENV SECRET_KEY 6e4#n(=+qal2tg1uyrxy*)r$)6co-j*o27sh2*u34*63#w!rfo

ENV DJANGO_SETTINGS_MODULE config.settings.docker

COPY ./docker/prod/web/uwsgi.ini /opt/webroms/uwsgi.ini
COPY ./docker/prod/web/domigrate.sh /opt/webroms
COPY ./docker/prod/web/createsuperuser.sh /opt/webroms

ENTRYPOINT ["uwsgi", "--ini", "uwsgi.ini"]

