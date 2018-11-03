from rest_framework import serializers

from . import models
from ..accounts.models import Employee
from ..accounts.serializers import EmployeeReadSerializer
from ..dishes.models import Dish
from ..dishes.serializers import DishSerializer


class RestaurantReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = '__all__'


class DishItemReadSerializer(serializers.ModelSerializer):
    dish = DishSerializer()

    class Meta:
        model = models.DishItem
        fields = '__all__'


class DishItemWriteSerializer(serializers.ModelSerializer):
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())

    class Meta:
        model = models.DishItem
        fields = ('dish', 'total',)

    def create(self, validated_data):
        instance, _ = models.DishItem.objects.get_or_create(**validated_data)
        return instance


class OrderReadSerializer(serializers.ModelSerializer):
    restaurant = RestaurantReadSerializer()
    employee = EmployeeReadSerializer()
    dishes = DishItemReadSerializer(many=True)
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = models.Order
        fields = '__all__'


class OrderWriteSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=models.Restaurant.objects.all())
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    dishes = serializers.PrimaryKeyRelatedField(queryset=models.DishItem.objects.all(), many=True)
    status = serializers.ChoiceField(choices=models.ORDER_STATUS_CHOICES)

    class Meta:
        model = models.Order
        fields = ('restaurant', 'employee', 'dishes', 'status')

    def create(self, validated_data):
        dishes = validated_data.pop('dishes')
        instance = models.Order.objects.create(**validated_data)
        for dish in dishes:
            instance.dishes.add(dish)
        return instance

    def update(self, instance, validated_data):
        dishes = validated_data.pop('dishes')
        for attr, value in validated_data.items():
            if value is not None:
                setattr(instance, attr, value)
        instance.save()
        for dish in dishes:
            instance.dishes.add(dish)
        return instance


