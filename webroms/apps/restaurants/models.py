from django.db import models
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Ресторан'
    )

    address = models.CharField(
        max_length=256,
        verbose_name='Адрес'
    )

    city = models.CharField(
        max_length=256,
        verbose_name='Город'
    )

    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DishItem(models.Model):
    dish = models.ForeignKey(
        'dishes.Dish',
        on_delete=models.CASCADE,
        verbose_name='Набор блюд'
    )

    total = models.DecimalField(
        default=1.0,
        max_digits=100,
        decimal_places=2,
        verbose_name='Количество'
    )
    updated = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    class Meta:
        ordering = ['-updated']
        unique_together = (('dish', 'total'),)


    @property
    def price(self):
        return self.total * self.dish.price

    def __str__(self):
        return '{}, кол-во: {}, сумм.: {} р.'.format(self.dish.title, self.total, self.price)


ORDER_STATUS_CHOICES = (
    ('created', 'Создан'),
    ('paid', 'Оплачен'),
    ('delivered', 'Заказ доставлен'),
    ('canceled', 'Отменен'),
)


class Order(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        verbose_name='Ресторан'
    )

    employee = models.ForeignKey(
        'accounts.Employee',
        on_delete=models.CASCADE,
        verbose_name='Сотрудник (оператор)'
    )

    dishes = models.ManyToManyField(
        DishItem,
        verbose_name='Набор блюд к заказу'
    )

    status = models.CharField(
        max_length=11,
        choices=ORDER_STATUS_CHOICES,
        verbose_name='Статус заказа'
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания заказа'
    )

    updated_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата обновления заказа'
    )

    objects = models.Manager()

    def __str__(self):
        return str(self.pk)

    @staticmethod
    def is_order():
        return True

    @property
    def total_amount(self):
        return sum([dish_item.price for dish_item in self.dishes.all()])

    class Meta:
        ordering = ['-updated_at']

    def save(self, **kwargs):
        self.updated_at = timezone.now()
        super(Order, self).save(**kwargs)
