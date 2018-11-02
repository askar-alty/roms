from django.contrib import admin
from reversion.admin import VersionAdmin

from . import models

# Register your models here.

admin.site.register(models.AuthToken)


@admin.register(models.Employee)
class EmployeeAdmin(VersionAdmin):
    def reversion_register(self, model, **options):
        options['exclude'] = ('user',)
        super().reversion_register(model, **options)
