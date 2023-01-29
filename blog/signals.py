from django.db.models.signals import pre_save
from django.dispatch import receiver

from blog.models import Tag
from extensions.utils import slug_generator


@receiver(pre_save, sender=Tag)
def save_tag_slug(sender, instance, *args, **kwargs):
    if instance.slug is None:
        print(instance.slug)
        instance.slug = slug_generator(instance.name)
