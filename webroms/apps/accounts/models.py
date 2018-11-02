from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.authtoken.models import Token


# Create your models here.


class Employee(models.Model):

    EMPLOYEE_POSITIONS_CHOICES = (
        ('operator', 'Оператор'),
        ('administrator', 'Администратор')
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee',
        verbose_name='Пользователь'
    )

    position = models.CharField(
        choices=EMPLOYEE_POSITIONS_CHOICES,
        max_length=14,
        verbose_name='Должность'
    )

    objects = models.Manager()

    class Meta:
        unique_together = (('user', 'position'),)

    def __str__(self):
        return '{}'.format(self.user)

    @staticmethod
    def is_employee():
        return True

    def is_admin(self):
        return self.position == 'administrator'

    def get_permissions(self):
        permissions = []
        for app_label in settings.APPS_LABELS_FOR_EMPLOYEE_POSITION_PERM.get(self.position, []):
            permissions += [permission for content_type in ContentType.objects.filter(app_label=app_label)
                            for permission in Permission.objects.filter(content_type=content_type)]
        return permissions

    def set_user_permissions(self):
        permissions = self.get_permissions()
        if len(permissions) and not self.user.is_superuser:
            self.user.user_permissions.clear()
            self.user.user_permissions.set(permissions)

    def save(self, **kwargs):
        self.set_user_permissions()
        self.user.is_active = True
        self.user.is_staff = True
        self.user.save()
        super(Employee, self).save(**kwargs)


class AuthTokenManager(models.Manager):

    def get_or_create(self, **kwargs):
        try:
            token = super(AuthTokenManager, self).get(**kwargs)
        except self.model.DoesNotExist:
            token = super(AuthTokenManager, self).create(**kwargs)
        return token


class AuthToken(Token):

    created = models.DateTimeField(default=timezone.now)
    expired = models.DateTimeField(default=timezone.now() + settings.API_TOKEN_LIFETIME)

    objects = AuthTokenManager()

    def is_expired(self):
        return (timezone.now().timestamp() - self.expired.timestamp()) > 0
