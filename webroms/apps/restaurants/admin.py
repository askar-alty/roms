from django.contrib import admin
from reversion.admin import VersionAdmin

from . import models

admin.site.register(models.Restaurant)
admin.site.register(models.DishItem)


@admin.register(models.Order)
class OrderAdmin(VersionAdmin):
    def reversion_register(self, model, **options):
        super().reversion_register(model, **options)
