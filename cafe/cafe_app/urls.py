from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, DishViewSet

# Инициализируем роутер
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'dishes', DishViewSet, basename='dish')

# Подключаем маршруты

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add/', views.add_order, name='add_order'),
    path('edit/<int:order_id>/', views.edit_order, name='edit_order'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('revenue/', views.revenue, name='revenue'),
    path('api/orders/search/', views.OrderSearchView.as_view(), name='order-search'),
    path('api/', include(router.urls)),  # Все API маршруты
]
