from django.db import models


class ActiveShopManager(models.Manager):
    def get_queryset(self):
        return super(ActiveShopManager, self).get_queryset().filter(status='a')
