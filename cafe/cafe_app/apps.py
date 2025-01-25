from django.apps import AppConfig


class CafeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cafe_app'
    verbose_name = 'Заказы кафе'

    def ready(self):
        import cafe_app.signals
