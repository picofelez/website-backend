from django.db import models


class PublishedProductsManager(models.Manager):
    def get_queryset(self):
        return super(PublishedProductsManager, self).get_queryset().filter(is_confirmed=True, is_active=True)
