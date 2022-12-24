from django.db import models
from django.utils.html import format_html

from account.models import User
from extensions.utils import upload_product_image_path
from product.managers import PublishedProductsManager
from shop.models import Shop


# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name='sub_cats', verbose_name='دسته بندی والد'
    )
    name = models.CharField(max_length=100, verbose_name='نام دسته')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = '2. دسته بندی ها'

    def __str__(self):
        return self.name


class Product(models.Model):
    shop = models.ForeignKey(
        Shop, on_delete=models.PROTECT, related_name='shop_products', verbose_name='فروشگاه'
    )
    maker = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='user_products', verbose_name='سازنده'
    )
    title = models.CharField(max_length=100, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    keywords = models.CharField(max_length=255, verbose_name='کلمات کلیدی')
    price = models.BigIntegerField(verbose_name='قیمت')
    stock = models.IntegerField(verbose_name='موجودی در انبار')
    quantity = models.CharField(max_length=50, verbose_name='واحد')
    weight = models.CharField(max_length=100, verbose_name='وزن')
    length = models.CharField(max_length=100, verbose_name='طول')
    width = models.CharField(max_length=100, verbose_name='ضخامت')
    image = models.ImageField(upload_to=upload_product_image_path, verbose_name='تصویر محصول')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    is_confirmed = models.BooleanField(default=True, verbose_name='تائید شده/نشده')
    categories = models.ManyToManyField(
        Category, related_name='products', verbose_name='دسته بندی ها'
    )
    purchase_limit = models.IntegerField(null=True, blank=True, verbose_name='محدودیت خرید')
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, null=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = '1. محصولات'

    objects = models.Manager()
    published = PublishedProductsManager()

    def get_thumbnail(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 5px;' src='{self.image.url}'>")

    get_thumbnail.short_description = "تصویر محصول"

    def get_price(self):
        return f"{self.price:,}"

    get_price.short_description = 'قیمت'

    def __str__(self):
        return self.title
