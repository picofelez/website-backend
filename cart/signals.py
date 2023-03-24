from django.db.models.signals import post_save
from django.dispatch import receiver

from cart.models import Transportation


@receiver(post_save, sender=Transportation)
def send_notif_to_shop_owner(sender, instance, created, *args, **kwargs):
    if created:
        text = f"یک سفارش جدید برای فروشگاه شما ایجاد شد، لطفا آن را بررسی کنید."
        # TODO: send sms.
        print(text)
