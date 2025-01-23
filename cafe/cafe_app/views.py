# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Order
from .forms import OrderForm

# Отображение списка всех заказов
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'cafe_app/order_list.html', {'orders': orders})






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
