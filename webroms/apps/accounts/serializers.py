from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email',)


class EmployeeReadSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Employee
        fields = '__all__'


class UserReadSerializer(serializers.ModelSerializer):
    employee = EmployeeReadSerializer()

    class Meta:
        model = models.User
        fields = ('username', 'employee')


class AuthTokenSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()

    class Meta:
        model = models.AuthToken
        fields = '__all__'
