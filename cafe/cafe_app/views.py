# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum, Q
from .models import Order
from .forms import OrderForm

# Отображение списка всех заказов
def order_list(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')  # Получаем выбранный статус

    query_lower = query.lower()
    # !!!!! При выборе SQlite в settings поиск будет чувствителен к регистру, поэтому я добавил второе поисковое слово с заглавной буквы
    query_capitalize = query.capitalize()

    if query:
        orders = Order.objects.prefetch_related('items').filter(
            Q(table_number__icontains=query) | Q(items__name__icontains=query_lower) | Q(items__name__icontains=query_capitalize)
        )
    else:
        orders = Order.objects.prefetch_related('items').all()

    if status:
        orders = orders.filter(status=status)

    return render(request, 'cafe_app/order_list.html', {'orders': orders, 'query': query})


def revenue(request):
    orders = Order.objects.prefetch_related('items').filter(status='paid')
    total_revenue = orders.aggregate(total=Sum('total_price'))['total'] or 0
    return render(request, 'cafe_app/revenue.html', {'orders': orders, 'total_revenue': total_revenue})




# Добавление нового заказа
def add_order(request):
    return order_process(request)



# Редактирование заказа
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return order_process(request, order)



def order_process(request, order=None):
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'cafe_app/order.html', {'form': form, 'order': order})


# Удаление заказа
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_list')
