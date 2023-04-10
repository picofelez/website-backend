from django.db import models
from django.utils import timezone


# Create your models here.
class WorkSample(models.Model):
    class StatusChoices(models.TextChoices):
        draft = 'd', 'چک نویس'
        published = 'p', 'منتشر شده'

    title = models.CharField(max_length=255, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to='portfolio/', verbose_name='تصویر')
    status = models.CharField(max_length=10, choices=StatusChoices.choices, verbose_name='وضعیت')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    address = models.CharField(max_length=75, null=True, blank=True, verbose_name='مکان')
    date = models.CharField(max_length=75, null=True, blank=True, verbose_name='تاریخ اجرا')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'نمونه کار'
        verbose_name_plural = '1. نمونه کار ها'

    def get_name_replace(self):
        return f"{self.title.replace(' ', '-')}"

    def __str__(self):
        return f"{self.title}"


class WorkSampleImage(models.Model):
    work_sample = models.ForeignKey(
        WorkSample, on_delete=models.CASCADE, related_name='images', verbose_name='نمونه کار'
    )
    image = models.ImageField(upload_to='portfolio/', verbose_name='تصویر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'تصویر نمونه کار'
        verbose_name_plural = '2. تصاویر نمونه کار'
