from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = '2. مدیریت فروشگاه ها'

    def ready(self):
        import shop.signals
