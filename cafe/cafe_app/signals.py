from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Order

@receiver(m2m_changed, sender=Order.items.through)
def calculate_total_price(sender, instance, **kwargs):
    """
    Пересчитывает общую стоимость заказа при добавлении или удалении блюд.
    """
    total_price = sum(dish.price for dish in instance.items.all())
    instance.total_price = total_price
    instance.save()
