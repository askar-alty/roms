# Generated by Django 2.1.2 on 2018-11-02 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название категории')),
                ('description', models.CharField(max_length=2000, null=True, verbose_name='Описание')),
                ('sub_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dishes.Category', verbose_name='Категрия категории')),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название блюда')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Цена')),
                ('description', models.CharField(max_length=2000, null=True, verbose_name='Описание')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата обновления заказа')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dishes.Category', verbose_name='Категрия категории')),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
    ]
