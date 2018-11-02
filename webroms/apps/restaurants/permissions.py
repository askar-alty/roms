from django.conf import settings
from rest_framework import permissions

from . import models

IsAuthenticated = permissions.IsAuthenticated


class ModelPermissions(permissions.DjangoObjectPermissions):
    perms_map = settings.PERMS_MAP
    model = models.DishItem

    def has_permission(self, request, view):
        perms = self.get_required_permissions(request.method, self.model)
        return request.user.has_perms(perms)


class DishItemPermissions(ModelPermissions):
    model = models.DishItem


class OrderPermissions(ModelPermissions):
    model = models.Order
