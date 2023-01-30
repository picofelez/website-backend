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
