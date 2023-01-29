from django.db import models
from extensions.utils import slug_generator


# Create your models here.
class Tag(models.Model):
    """
    The Tag main model.
    """
    name = models.CharField(max_length=75, verbose_name='نام تگ')
    slug = models.SlugField(null=True, blank=True, verbose_name='شناسه')

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = '1. برچسب ها'

    def __str__(self):
        return self.name
