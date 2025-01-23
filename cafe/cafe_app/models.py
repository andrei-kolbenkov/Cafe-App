from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

class Dish(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название блюда')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField(verbose_name='Номер стола')
    items = models.ManyToManyField('Dish', verbose_name='Заказанные блюда')  # Связь многие ко многим
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting', verbose_name='Статус заказа')



    def __str__(self):
        return f'Заказ {self.id} для стола {self.table_number} ======= {self.total_price} р.'



