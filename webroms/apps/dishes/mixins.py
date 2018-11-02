from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from reversion.views import RevisionMixin

RevisionMixin = RevisionMixin


class RequiredMixin(PermissionRequiredMixin, LoginRequiredMixin):
    redirect_field_name = '/accounts/login/?next=%s'
    permission_required = ('dishes.view_category', 'dishes.view_dish',)
