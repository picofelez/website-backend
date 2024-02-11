import random

from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify

from extensions.utils import upload_product_image_path, generate_product_id, jalali_converter
from product.managers import PublishedProductsManager
from shop.models import Shop

# Create your models here.
User = get_user_model()


class Category(models.Model):
    """
    The category main model.
    """
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name='sub_cats', verbose_name='دسته بندی والد'
    )
    name = models.CharField(max_length=100, verbose_name='نام دسته')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    description = RichTextField(null=True, blank=True, verbose_name='توضیحات')
    slug = models.SlugField(
        max_length=255, null=True, blank=True, verbose_name="اسلاگ"
    )
    meta_keywords = models.CharField(max_length=255, null=True, blank=True, verbose_name='کلمات کلیدی')
    meta_description = models.CharField(max_length=255, null=True, blank=True, verbose_name='توضیحات')
    meta_title = models.CharField(max_length=255, null=True, blank=True, verbose_name='عنوان متا')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = '2. دسته بندی ها'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:work-sample-category-list", args=[self.slug, self.pk])

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    The product main model,
    Many-To-One relationship with Shop,
    Many-to-One relationship with User,
    Many-To-Many relationship wit Category.
    """

    class ProductTypeChoices(models.TextChoices):
        multiple_seller = 'multiple', 'چند فروشنده'
        solo_seller = 'solo', 'تک فروشنده'

    id = models.CharField(
        max_length=255, default=generate_product_id, primary_key=True, editable=False, unique=True
    )
    shop = models.ForeignKey(
        Shop, on_delete=models.PROTECT, null=True, blank=True, related_name='shop_products', verbose_name='فروشگاه'
    )
    maker = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, related_name='user_products', verbose_name='سازنده'
    )
    title = models.CharField(max_length=100, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    keywords = models.CharField(max_length=255, null=True, blank=True, verbose_name='کلمات کلیدی')
    price = models.BigIntegerField(verbose_name='قیمت', null=True, blank=True, )
    stock = models.IntegerField(verbose_name='موجودی در انبار', null=True, blank=True, )
    quantity = models.CharField(max_length=50, verbose_name='واحد', null=True, blank=True)
    weight = models.CharField(max_length=100, verbose_name='وزن', null=True, blank=True)
    length = models.CharField(max_length=100, verbose_name='طول', null=True, blank=True)
    width = models.CharField(max_length=100, verbose_name='ضخامت', null=True, blank=True)
    image = models.ImageField(upload_to=upload_product_image_path, null=True, blank=True, verbose_name='تصویر محصول')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    is_confirmed = models.BooleanField(default=True, verbose_name='تائید شده/نشده')
    categories = models.ManyToManyField(
        Category, related_name='products', verbose_name='دسته بندی ها'
    )
    purchase_limit = models.IntegerField(null=True, blank=True, verbose_name='محدودیت خرید')
    product_type = models.CharField(
        max_length=20, choices=ProductTypeChoices.choices, default=ProductTypeChoices.solo_seller, verbose_name='نوع'
    )
    shops = models.ManyToManyField(
        Shop, related_name='multiple_products', verbose_name='فروشنده ها'
    )
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, null=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = '1. محصولات'
        ordering = ('-created',)

    objects = models.Manager()
    published = PublishedProductsManager()

    def get_thumbnail(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 5px;' src='{self.image.url}'>")

    get_thumbnail.short_description = "تصویر محصول"

    def get_price(self):
        if self.price:
            return f"{self.price:,}"
        return 0

    get_price.short_description = 'قیمت'

    def get_absolute_url(self):
        if self.product_type == 'solo':
            return reverse('product:product-detail', args=[self.id, self.get_replaced_title()])
        elif self.product_type == 'multiple':
            return reverse('product:multiple-product-detail', args=[self.id, self.get_replaced_title()])

    def get_replaced_title(self):
        return self.title.replace(' ', '-')

    def __str__(self):
        return f"{self.title} - {self.shop if self.shop else f'{self.shops.count()} فروشنده'}"


class FavoriteProduct(models.Model):
    """
    The FavoriteProduct main model,
    Many-To-One relationship with User,
    Many-To-One relationship with product.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites', verbose_name='کاربر'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='user_favorites', verbose_name='محصول'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'محصول مورد علاقه'
        verbose_name_plural = '3. محصولات مورد علاقه'
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user.get_full_name()} | {self.product.title}"


class PriceHistory(models.Model):
    """
    The Product Price History main model.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_histories', verbose_name='محصول')
    price = models.BigIntegerField(verbose_name='قیمت')
    is_confirmed = models.BooleanField(verbose_name='تائید شده/نشده')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'تغیر قیمت'
        verbose_name_plural = '4. تغییرات قیمت'

    def created_jalali(self):
        return jalali_converter(self.created)

    def __str__(self):
        return f"{self.product.title} - {self.price:,}"
