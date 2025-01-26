from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from django.db.models import Sum, Q
from typing import Union, Optional
import pytest
from .models import Order, Dish
from .serializers import OrderSerializer, DishSerializer
from .forms import OrderForm

# Отображение списка всех заказов
def order_list(request: HttpRequest) -> HttpResponse:
    """
    Отображает список заказов с возможностью фильтрации по номеру стола, статусу и названиям блюд.

    Аргументы:
        request (HttpRequest): Объект HTTP-запроса с возможными GET-параметрами:
            - `q`: строка для поиска по номеру стола или названию блюда.
            - `status`: строка, задающая фильтр по статусу заказа.

    Примечания:
        - !!!!! При выборе SQlite в settings поиск будет чувствителен к регистру, поэтому я добавил второе поисковое слово с заглавной буквы
        - Предварительно подгружаются связанные объекты `items` для оптимизации запросов.
    """
    query: str = request.GET.get('q', '').strip()
    status: str = request.GET.get('status', '')

    query_lower: str = query.lower()
    query_capitalize: str = query.capitalize()

    if query:
        orders = Order.objects.prefetch_related('items').filter(
            Q(table_number__icontains=query) | Q(items__name__icontains=query_lower) | Q(items__name__icontains=query_capitalize)
        )
    else:
        orders = Order.objects.prefetch_related('items').all()

    if status:
        orders = orders.filter(status=status)

    return render(request, 'cafe_app/order_list.html', {'orders': orders, 'query': query})


def revenue(request: HttpRequest) -> HttpResponse:
    """
    Отображает страницу с общей выручкой от оплаченных заказов.
    Примечания:
        - Фильтруются только заказы со статусом `paid`.
        - Вычисляется общая сумма через агрегатную функцию `Sum`.
    """
    orders = Order.objects.prefetch_related('items').filter(status='paid')
    total_revenue: float = orders.aggregate(total=Sum('total_price'))['total'] or 0
    return render(request, 'cafe_app/revenue.html', {'orders': orders, 'total_revenue': total_revenue})




# Добавление нового заказа
def add_order(request: HttpRequest) -> HttpResponse:
    # Отвечает за добавление нового заказа, вызывая общую логику обработки заказа.
    return order_process(request)



# Редактирование заказа
def edit_order(request: HttpRequest, order_id: int) -> HttpResponse:
    """
        Отвечает за редактирование существующего заказа.

        Аргументы:
            request (HttpRequest): Объект HTTP-запроса.
            order_id (int): ID редактируемого заказа.

        Возвращает:
            HttpResponse: Ответ, обработанный функцией `order_process`.

        Исключения:
            - Возвращает 404, если заказ с указанным ID не найден.
        """
    order = get_object_or_404(Order, id=order_id)
    return order_process(request, order)



def order_process(request: HttpRequest, order: Optional[Order] = None) -> HttpResponse:
    """
    Общая логика добавления и редактирования заказа.

    Аргументы:
        request (HttpRequest): Объект HTTP-запроса.
        order (Optional[Order]): Экземпляр заказа для редактирования, либо `None` для добавления нового заказа.

    """
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'cafe_app/order.html', {'form': form, 'order': order})


# Удаление заказа
def delete_order(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Удаляет заказ по его ID. Возвращает 404, если заказ с указанным ID не найден.
    Аргументы:
        request (HttpRequest): Объект HTTP-запроса.
        order_id (int): ID удаляемого заказа.
    """
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_list')



class OrderViewSet(ModelViewSet):
    """
        API для управления заказами.

        Атрибуты:
            queryset (QuerySet): Список всех заказов с предварительно загруженными блюдами.
            serializer_class (Type[Serializer]): Сериализатор для преобразования заказов.
    """
    queryset = Order.objects.prefetch_related('items')  # Список всех заказов с предварительно загруженными блюдами.
    serializer_class = OrderSerializer # Сериализатор для преобразования заказов.


class DishViewSet(ModelViewSet):
    """
        API для управления блюдами.

        Атрибуты:
            queryset (QuerySet): Список всех блюд.
            serializer_class (Type[Serializer]): Сериализатор для преобразования блюд.
    """
    queryset = Dish.objects.all() # Список всех блюд.
    serializer_class = DishSerializer # Сериализатор для преобразования блюд.



class OrderSearchView(ListAPIView):
    """
       API для поиска заказов с возможностью фильтрации и поиска.
       Атрибуты:
           queryset (QuerySet): Список всех заказов с предварительно загруженными блюдами.
           serializer_class (Type[Serializer]): Сериализатор для преобразования заказов.
           filter_backends (List[Type[BaseFilterBackend]]): Список используемых фильтров.
           filterset_fields (List[str]): Поля, доступные для фильтрации.
           search_fields (List[str]): Поля, доступные для поиска.
   """
    queryset = Order.objects.prefetch_related('items').all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['table_number', 'status']  # Фильтрация по полям
    search_fields = ['items__name', 'table_number']  # Поиск