from django import forms
from .models import Order, Dish
from django.utils.safestring import mark_safe


class DishCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    """
    Класс для переопределения стандартного виджета CheckboxSelectMultiple с добавлением атрибута `data-price` для каждого элемента.
    """

    def render(self, name: str, value: list, attrs: dict = None, renderer: object = None) -> str:
        """
        Переопределяет метод `render` для добавления атрибута `data-price` к каждому элементу списка чекбоксов.

        Args:
            name (str): Имя поля формы.
            value (list): Текущее значение поля (выбранные элементы).
            attrs (dict, optional): Атрибуты HTML для поля. По умолчанию None.
            renderer (object, optional): Рендерер для генерации HTML. По умолчанию None.
        """
        # Генерируем базовый HTML с использованием стандартного метода.
        output = super().render(name, value, attrs, renderer)

        # Получаем queryset блюд из привязанного набора данных выбора.
        dishes = self.choices.queryset

        # Для каждого блюда добавляем атрибут `data-price` в HTML-код.
        for dish in dishes:
            price = dish.price
            output = output.replace(
                f'value="{dish.id}"',
                f'value="{dish.id}" data-price="{price}"'
            )
            # Добавляем цену к названию блюда
            output = output.replace(
                f'{dish.name}',
                f'{dish.name} — {price} р.'
            )

        # Возвращаем безопасный HTML-код.
        return mark_safe(output)




class OrderForm(forms.ModelForm):
    """
       Форма для создания и редактирования заказов. Включает выбор блюд, номер стола, статус и итоговую сумму.
       Использует настраиваемый виджет для поля выбора блюд.
    """
    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status', 'total_price']
        widgets = {
            'items': DishCheckboxSelectMultiple,  # Позволяет выбрать несколько блюд с помощью чекбоксов
        }







