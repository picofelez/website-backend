import uuid

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Shop


@receiver(pre_save, sender=Shop)
def save_shop_unique_id(sender, instance, *args, **kwargs):
    if instance.unique_uuid is None:
        print(uuid.uuid4())
        instance.unique_uuid = uuid.uuid4()
