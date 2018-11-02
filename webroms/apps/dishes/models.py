from django.db import models


# Create your models here.
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )

    description = models.CharField(
        max_length=2000,
        null=True,
        verbose_name='Описание'
    )

    sub_category = models.ForeignKey(
        'self',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Категрия категории'
    )

    objects = models.Manager()

    def __str__(self):
        return self.title


class Dish(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='Название блюда'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категрия категории'
    )

    price = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        default=0.0,
        verbose_name='Цена'
    )

    description = models.CharField(
        max_length=2000,
        null=True,
        verbose_name='Описание'
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата обновления заказа'
    )

    objects = models.Manager()

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title
