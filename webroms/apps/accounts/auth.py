import re

from django.utils.six import text_type
from django.utils.translation import ugettext_lazy as _
from rest_framework import authentication, exceptions

from .models import AuthToken


def get_authorization_header(request):
    key = request.META.get('HTTP_API_TOKEN')
    if not isinstance(key, text_type) or not re.match(r'[a-zA-Z0-9]{40,}', key):
        msg = _('Invalid token header. Token string should not contain invalid characters.')
        raise exceptions.AuthenticationFailed(msg)

    return key


class TokenAuth(authentication.BaseAuthentication):

    def authenticate(self, request):
        key = get_authorization_header(request)
        if not key:
            return None, None
        try:
            token = AuthToken.objects.get(key=key)
        except AuthToken.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        if token.is_expired():
            raise exceptions.AuthenticationFailed(
                _(
                    'Token is expired. Try to login again using by username and password. Valid path to login is /api/login'))
        return (token.user, token)
