from urllib.parse import urlencode

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

from .. import models


def to_url_params(data):
    return urlencode(data)


def to_multi_params(data):
    query = QueryDict('', mutable=True)
    query.update(MultiValueDict(data))
    return query.urlencode()


def cases(data):
    if callable(data):
        data = data()

    if not all(isinstance(i, dict) for i in data):
        raise Exception("Need a sequence of tuples as mac-vendors...")

    def test_decorator(func):
        def test_decorated(self, *args, **kwargs):
            for test_case in data:
                func(self, test_case)

        return test_decorated

    return test_decorator


def create_user(username, password):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, email='testt@mail.test', password=password)
    return user


def add_user_permissions(user):
    content_type = ContentType.objects.get_for_model(models.Device)
    for codename, name in [('add_' + models.Employee._meta.model_name,
                            'Can add ' + models.Employee._meta.model_name),
                           ('change_' + models.Employee._meta.model_name,
                            'Can change ' + models.Employee._meta.model_name),
                           ('view_' + models.Employee._meta.model_name,
                            'Can view ' + models.Employee._meta.model_name)]:
        try:
            permission = Permission.objects.get(**{'content_type': content_type, 'codename': codename})
        except Permission.DoesNotExist:
            permission = Permission.objects.create(name=name, content_type=content_type, codename=codename)

        user.user_permissions.add(permission)
