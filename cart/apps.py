from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
    verbose_name = '6. مدیریت بخش خرید'

    def ready(self):
        import cart.signals
