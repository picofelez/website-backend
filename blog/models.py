from django.db import models
from django.utils import timezone
from django.utils.html import format_html


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


class Article(models.Model):
    """
    The Article main model,
    Many-To-Many relationship with Tag model.
    """

    class StatusChoices(models.TextChoices):
        published = 'a', 'منتشر شده'
        draft = 'd', 'چک نویس'

    title = models.CharField(max_length=155, verbose_name='عنوان')
    summary = models.CharField(max_length=255, verbose_name='خلاصه')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to='', verbose_name='تصویر اصلی')
    tags = models.ManyToManyField(
        Tag, related_name='articles', verbose_name='برچسب ها'
    )
    status = models.CharField(max_length=5, choices=StatusChoices.choices, verbose_name='وضعیت انتشار')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = '2. مقالات'

    def __str__(self):
        return self.title

    def get_thumbnail(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 5px;' src='{self.image.url}'>")

    get_thumbnail.short_description = "تصویر"
