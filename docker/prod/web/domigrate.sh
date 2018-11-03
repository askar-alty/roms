#!/bin/bash

export SECRET_KEY='6e4#n(=+qal2tg1uyrxy*)r$)6co-j*o27sh2*u34*63#w!rfo'
python manage.py makemigrations --settings=config.settings.docker&&python manage.py migrate --settings=config.settings.docker