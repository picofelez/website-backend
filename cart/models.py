from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Address(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, related_name='addresses', verbose_name='کاربر'
    )
    city = models.CharField(max_length=50, verbose_name='شهر')
    full_address = models.TextField(verbose_name='آدرس کامل')
    zip_code = models.CharField(max_length=20, verbose_name='کد پستی')
    phone_number = models.CharField(max_length=20, verbose_name='شماره تماس')
    name = models.CharField(max_length=50, verbose_name='نام تحویل گیرنده')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'
        ordering = ('-created',)

    def __str__(self):
        return f"{self.name} | {self.city}"
