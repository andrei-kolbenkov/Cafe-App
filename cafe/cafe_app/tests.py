import pytest
from django.urls import reverse
from django.test import Client
from cafe_app.models import Order, Dish
from django.contrib.auth.models import User

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
def dish1(db):
    return Dish.objects.create(name='Чизкейк', price=10)

@pytest.fixture
def dish2(db):
    """Создаем второе блюдо для теста."""
    return Dish.objects.create(name='Чай', price=2)

@pytest.fixture
def order(db, dish1):
    order = Order.objects.create(table_number=1, status='waiting')
    order.items.add(dish1)
    return order


# Тесты для функции order_list
def test_order_list_with_query(client, order):
    url = reverse('order_list')
    response = client.get(url, {'q': 'Чизкейк'})
    assert response.status_code == 200
    assert 'Чизкейк' in response.content.decode()

def test_order_list_with_status(client, order):
    url = reverse('order_list')
    response = client.get(url, {'status': 'paid'})
    assert response.status_code == 200

# # Тесты для функции revenue
def test_revenue_view(client, order, dish2):
    # Прокачиваем первый заказ в статус 'paid', если еще не был в таком статусе
    order.status = 'paid'
    order.save()
    # Создаем второй заказ и ставим его в статус 'paid'
    second_order = Order.objects.create(table_number=2, status='paid', total_price=200)
    second_order.items.add(dish2)
    url = reverse('revenue')
    response = client.get(url)
    assert response.status_code == 200
    # Проверяем, что в контексте передана правильная сумма выручки
    total_revenue = response.context['total_revenue']
    expected_revenue = order.total_price + second_order.total_price  # Ожидаем, что сумма выручки = сумма двух заказов
    assert total_revenue == expected_revenue
    # Проверяем, что сумма отображается в контенте страницы
    assert str(total_revenue) in response.content.decode()


# Тесты для функции add_order
@pytest.mark.django_db
def test_add_order_with_dishes(client, dish1, dish2):
    # Делаем GET-запрос, чтобы получить форму для добавления заказа
    order_url = reverse('add_order')
    response = client.get(order_url)
    assert response.status_code == 200
    assert 'form' in response.context

    # Подготавливаем данные для формы (выбираем два блюда и указываем номер стола)
    post_data = {
        'table_number': 1,
        'items': [dish1.id, dish2.id],
        'status': "waiting"
    }

    # Делаем POST-запрос с данными формы
    response = client.post(order_url, post_data)

    # Проверяем, что запрос был успешным и мы перенаправлены на список заказов
    assert response.status_code == 302  # Ожидаем редирект
    assert response['Location'] == reverse('order_list')


    # Проверяем, что заказ был добавлен в базу данных
    order = Order.objects.last()  # Получаем последний добавленный заказ
    assert order.table_number == 1
    assert order.status == 'waiting'

    # Проверяем, что выбранные блюда правильно связаны с заказом
    assert order.items.count() == 2
    assert dish1 in order.items.all()
    assert dish2 in order.items.all()

    # Проверяем, что общая стоимость заказа была вычислена корректно
    expected_total_price = dish1.price + dish2.price
    assert order.total_price == expected_total_price

#
# # Тесты для функции edit_order
@pytest.mark.django_db
def test_edit_order(client, user, order, dish1, dish2):
    # Получаем URL для редактирования заказа
    edit_url = reverse('edit_order', args=[order.id])  # Используем ID заказа для редактирования
    response = client.get(edit_url)

    # Проверяем, что форма для редактирования открыта
    assert response.status_code == 200
    assert 'form' in response.context

    post_data = {
        'table_number': 2,  # Меняем номер стола
        'status': 'waiting',  # Статус остается таким же
        'items': [dish1.id, dish2.id]
    }

    # Делаем POST-запрос с новыми данными
    response = client.post(edit_url, post_data)
    assert response.status_code == 302
    assert response['Location'] == reverse('order_list')

    updated_order = Order.objects.get(id=order.id)
    assert updated_order.table_number == 2  # Новый номер стола


#
# # Тесты для функции delete_order
def test_delete_order(client, user, order):
    url = reverse('delete_order', args=[order.id])
    response = client.post(url)
    assert response.status_code == 302
    assert not Order.objects.filter(id=order.id).exists()



# Тесты для API-классов
def test_order_viewset_list(client, order):
    url = reverse('order-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.django_db
def test_create_order(client, dish1):
    url = reverse('order-list')  # POST-запрос на создание заказа
    post_data = {
        'table_number': 3,
        'items': [dish1.id],
        'status': ''
    }
    response = client.post(url, post_data, format='json')

    assert response.status_code == 201  # Ожидаем статус 201 (создано)
    assert response.data['table_number'] == 3
    assert float(response.data['total_price']) == dish1.price
    assert response.data['status'] == 'waiting'


@pytest.mark.django_db
def test_update_order(client, order, dish2):
    url = reverse('order-detail', args=[order.id])  # PUT-запрос на обновление заказа
    post_data = {
        'table_number': 4,  # Обновляем номер стола
        'items': [dish2.id],  # Меняем блюда
    }
    response = client.put(url, post_data, content_type='application/json')

    assert response.status_code == 200  # Ожидаем статус 200 (успешное обновление)
    assert response.data['table_number'] == 4
    assert float(response.data['total_price']) == dish2.price


@pytest.mark.django_db
def test_delete_order(client, order):
    url = reverse('order-detail', args=[order.id])  # DELETE-запрос на удаление заказа
    response = client.delete(url)

    assert response.status_code == 204  # Ожидаем статус 204 (успешное удаление)
    assert Order.objects.filter(id=order.id).count() == 0  # Проверяем, что заказ удален


#
def test_dish_viewset_list(client, dish1):
    url = reverse('dish-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) > 0

@pytest.mark.django_db
def test_create_dish(client):
    url = reverse('dish-list')  # POST-запрос на создание блюда
    post_data = {
        'name': 'Суши',
        'price': 10,
    }
    response = client.post(url, post_data, format='json')

    assert response.status_code == 201  # Ожидаем статус 201 (создано)
    assert response.data['name'] == 'Суши'
    assert float(response.data['price']) == 10

@pytest.mark.django_db
def test_update_dish(client, dish2):
    url = reverse('dish-detail', args=[dish2.id])  # PUT-запрос на обновление заказа
    post_data = {
        'name': 'Чай',
        'price': 3,
    }
    response = client.put(url, post_data, content_type='application/json')

    assert response.status_code == 200
    assert response.data['name'] == 'Чай'
    assert float(response.data['price']) == 3


@pytest.mark.django_db
def test_delete_dish(client, dish2):
    url = reverse('dish-detail', args=[dish2.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert Order.objects.filter(id=dish2.id).count() == 0

#
def test_order_search_api(client, order):
    url = reverse('order-search')
    response = client.get(url, {'search': 'Чизкейк'})
    assert response.status_code == 200
    assert len(response.json()) > 0


