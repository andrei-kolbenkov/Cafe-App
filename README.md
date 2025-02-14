# Cafe-App
Этот репозиторий представляет собой Django проект для управления заказами и блюдами в ресторане. В нем реализован RESTful API, а также интерфейс через шаблоны и представления для управления заказами, блюдами и данными о выручке. Подробное описание функций указано в коде, в том числе с использованием аннотаций

**URL's:**
- ' '  - Список заказов
- add/ - Добавить заказ
- edit/{order_id}>/ - Редактировать заказ
- delete/{order_id}>/ - Удалить заказ
- revenue/ - Подсчет выручки
- admin/ - Админ панель
- swagger/ 
- redoc/

**API**
- GET /api/orders/ - Получение списка всех заказов. 
- GET /api/orders/{order_id}/ - Получение подробной информации о заказе по его ID.
- POST /api/orders/ - Создание нового заказа. Поле 'status' по умолчанию "waiting". Тело запроса:

{
    "table_number": 3,
    "items": [1, 2],
    "status": "waiting"
}
- PUT /api/orders/{order_id}/ - Обновление существующего заказа.
- DELETE /api/orders/{order_id}/ - Удаление существующего заказа.

- GET /api/dishes/ - Получение списка всех блюд.
- GET /api/dishes/{dish_id}/ - Получение подробной информации о блюде по его ID.
- POST /api/dishes/ - Создание нового блюда. Тело запроса:

{
    "name": "Пицца",
    "price": 20.00
}
- PUT /api/dishes/{dish_id}/ -  Обновление существующего блюда.
- DELETE /api/dishes/{dish_id}/ - Удаление существующего блюда
- GET /api/orders/search/ - Поиск заказов по ключевому слову. Используется для фильтрации заказов по статусу, номеру стола. Примеры: 
*api/orders/search/?table_number=5*  , *api/orders/search/?table_number=5&status=waiting*,  api/orders/search/?table_number=5&status=waiting&search=Пицца



Развертывание приложения:
1. Создайте виртуальное окружение (если у вас его еще нет):
python3 -m venv venv
2. Установите все зависимости из файла requirements.txt 
pip install -r requirements.txt
3. Настройте базу данных в settings.py. Учтите, что выбор влияет на некоторые представления. Подробнее в файле views.py
4. Если используете вложенный файл SQlite, то при авторизации в админ панель используйте логин и пароль admin 12345, если используете новую БД, создайте суперпользователя командой python manage.py createsuperuser, перейдя в директорию с проектом.
5. Запустите сервер разработки Django, чтобы убедиться, что приложение работает правильно: Перейдите по адресу http://127.0.0.1:8000/ в вашем браузере, чтобы проверить работу приложения.
Тестирование

Для тестирования функционала используется pytest и Django test client. 
Файл pytest.ini - конфигурация. Используйте команду pytest в директории с проектом для проведения тестов 