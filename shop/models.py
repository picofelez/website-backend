from django.db import models
from django.utils.html import format_html

from account.models import User
from extensions import upload_shop_image_path


# Create your models here.


class Shop(models.Model):
    class StatusChoices(models.TextChoices):
        active = 'a', 'فعال'
        deactivate = 'da', 'غیرفعال'
        block = 'b', 'بلاک شده'
        spam = 's', 'اسپم'

    title = models.CharField(max_length=155, verbose_name='نام نمایشی فروشگاه')
    slug = models.SlugField(null=True, blank=True, unique=True, verbose_name='شناسه اسلاگ')
    image = models.ImageField(upload_to=upload_shop_image_path, verbose_name='تصویر')
    owner = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='shops', verbose_name='مدیر فروشگاه'
    )
    location = models.CharField(max_length=100, verbose_name='مکان')
    status = models.CharField(
        max_length=4, choices=StatusChoices.choices, default=StatusChoices.active, verbose_name='وضعیت فروشگاه'
    )
    about = models.TextField(verbose_name='متن دباره ما')
    is_special = models.BooleanField(default=False, null=True, blank=True, verbose_name='برگزیده')
    is_special_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ برگزیده شدن')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name = 'فروشگاه'
        verbose_name_plural = '1. فروشگاه ها'
        ordering = ('-created',)

    def get_thumbnail(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 5px;' src='{self.image.url}'>")

    get_thumbnail.short_description = "تصویر فروشگاه"

    def __str__(self):
        return self.title
