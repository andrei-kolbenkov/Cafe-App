from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название блюда')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"


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

    def save(self, *args, **kwargs):
        """
        Переопределяем метод save для пересчёта общей стоимости заказа.
        """
        # Пересчитываем общую стоимость только если заказ имеет блюда
        if self.pk:  # Проверяем, существует ли объект (чтобы избежать проблем при создании)
            self.total_price = sum(dish.price for dish in self.items.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Заказ {self.id} для стола {self.table_number} ======= {self.total_price} р.'


    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"





