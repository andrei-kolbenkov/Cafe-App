from django import forms
from .models import Order, Dish
from django.utils.safestring import mark_safe

class DishCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        dishes = self.choices.queryset
        for dish in dishes:
            price = dish.price
            output = output.replace(
                f'value="{dish.id}"',
                f'value="{dish.id}" data-price="{price}"'
            )
        return mark_safe(output)



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status', 'total_price']
        widgets = {
            'items': DishCheckboxSelectMultiple,  # Позволяет выбрать несколько блюд с помощью чекбоксов
        }







