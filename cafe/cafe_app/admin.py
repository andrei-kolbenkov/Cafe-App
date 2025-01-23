from django.contrib import admin
from .models import Order, Dish
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['total_price']

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    pass

