from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class Question(models.Model):
    """
    The Question main model.
    """

    class StatusChoices(models.TextChoices):
        active = 'a', 'فعال'
        deactivate = 'da', 'غیرفعال'

    title = models.CharField(max_length=120, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    status = models.CharField(
        max_length=5, choices=StatusChoices.choices, default=StatusChoices.active, verbose_name='وضعیت نمایش'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات متداول'

    def __str__(self):
        return self.title


class Rating(models.Model):
    """
    The Rating main model,
    GenericRelation.
    """
    stars = models.IntegerField(null=True, blank=True, verbose_name='ستاره ها')
    comment = models.TextField(null=True, blank=True, verbose_name='کامنت')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیاز ها'

    def __str__(self):
        return f"{self.content_type}"
