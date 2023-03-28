import uuid

from django.db import models
from django.utils.html import format_html

from account.models import User
from extensions.utils import upload_shop_image_path, jalali_converter
from .managers import ActiveShopManager


# Create your models here.


class Shop(models.Model):
    """
    The Shop main model,
    Many-To-One relationship with User.
    """

    class StatusChoices(models.TextChoices):
        active = 'a', 'فعال'
        deactivate = 'da', 'غیرفعال'
        block = 'b', 'بلاک شده'
        spam = 's', 'اسپم'

    unique_uuid = models.UUIDField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=155, verbose_name='نام نمایشی فروشگاه')
    slug = models.SlugField(null=True, blank=True, unique=True, verbose_name='شناسه اسلاگ')
    image = models.ImageField(upload_to=upload_shop_image_path, null=True, blank=True, verbose_name='تصویر')
    owner = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='shops', verbose_name='مدیر فروشگاه'
    )
    location = models.CharField(max_length=100, verbose_name='مکان')
    status = models.CharField(
        max_length=4, choices=StatusChoices.choices, default=StatusChoices.active, verbose_name='وضعیت فروشگاه'
    )
    demand = models.TextField(
        null=True, blank=True, verbose_name='تقاضا'
    )
    supply = models.TextField(
        null=True, blank=True, verbose_name='عرضه'
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

    objects = models.Manager()
    active = ActiveShopManager()

    def get_thumbnail(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 5px;' src='{self.image.url}'>")

    get_thumbnail.short_description = "تصویر فروشگاه"

    def __str__(self):
        return self.title


class Contact(models.Model):
    """
    The contact main model,
    Many-To-One relationship with Shop.
    """

    class StatusChoices(models.TextChoices):
        read = 'r', 'خوانده شده'  # read
        unread = 'ur', 'خوانده نشده'  # unread

    full_name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    subject = models.CharField(max_length=100, verbose_name='موضوع')
    phone = models.CharField(max_length=12, verbose_name='شماره تلفن')  # phone number
    message = models.TextField(verbose_name='پیام')
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, null=True, blank=True, related_name='contacts', verbose_name='فروشگاه گیرنده'
    )
    status = models.CharField(
        max_length=4, choices=StatusChoices.choices, default=StatusChoices.unread, verbose_name='وضعیت مشاهده'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = '2. پیام ها'
        ordering = ('-created',)

    def __str__(self):
        return self.full_name


class SellerInformation(models.Model):
    """
    The SellerInformation main model,
    Many-To-One relationship with Shop.
    """

    phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن')
    full_name = models.CharField(max_length=255, verbose_name='نام و نام خانوادگی')
    national_code = models.CharField(max_length=10, verbose_name='کدملی')
    shop = models.ForeignKey(
        Shop, on_delete=models.PROTECT, related_name='sellers', verbose_name='فروشگاه'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name_plural = '3. اطلاعات فروشندگان'
        verbose_name = 'اطلاعات فروشنده'

    def __str__(self):
        return f"{self.shop} | {self.full_name}"


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='wallets', verbose_name='کاربر'
    )
    shop = models.ForeignKey(
        Shop, on_delete=models.PROTECT, related_name='shops', verbose_name='فروشگاه'
    )
    balance = models.BigIntegerField(default=0, verbose_name='موجودی')
    sheba = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره شبا')
    confirmed = models.BooleanField(verbose_name='تائید شده/نشده')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name_plural = '4. کیف پول ها'
        verbose_name = 'کیف پول'

    def created_jalali(self):
        return f"{jalali_converter(self.created)} ساعت {self.created.hour}:{self.created.minute}"

    created_jalali.short_description = 'تاریخ ایجاد'

    def get_balance(self):
        return f"{self.balance:,} ت"

    get_balance.short_description = 'موجودی'

    def deposit(self, value):
        self.transactions.create(
            value=value,
            running_balance=self.balance + value,
            transaction_type='d',  # deposit
            transaction_status=True
        )
        self.balance += value
        self.save()

    def withdraw(self, value):
        if value <= self.balance:
            self.transactions.create(
                value=value,
                running_balance=self.balance - value,
                transaction_type='w',  # withdraw
                transaction_status=False
            )

    def __str__(self):
        return f"{self.user.get_full_name()} | {self.shop.title}"


class WalletTransaction(models.Model):
    class TransactionTypeChoices(models.TextChoices):
        deposit = 'd', 'واریز'
        withdraw = 'w', 'برداشت'

    wallet = models.ForeignKey(
        Wallet, on_delete=models.PROTECT, related_name='transactions', verbose_name='کیف پول'
    )
    value = models.BigIntegerField(verbose_name='مبلغ')
    running_balance = models.BigIntegerField(verbose_name='موجودی بعد از تراکنش')
    transaction_type = models.CharField(max_length=2, choices=TransactionTypeChoices.choices, verbose_name='نوع تراکنش')
    transaction_status = models.BooleanField(verbose_name='وضعیت انجام تراکنش')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name_plural = '5. تراکنش های کیف پول'
        verbose_name = 'تراکنش کیف پول'
        ordering = ('-created',)

    def created_jalali(self):
        return f"{jalali_converter(self.created)} ساعت {self.created.hour}:{self.created.minute}"

    created_jalali.short_description = 'تاریخ ایجاد'

    def updated_jalali(self):
        return f"{jalali_converter(self.updated)} ساعت {self.updated.hour}:{self.updated.minute}"

    updated_jalali.short_description = 'تاریخ انجام تراکنش'

    def get_value(self):
        return f"{self.value:,} ت"

    get_value.short_description = 'مبلغ تراکنش'

    def __str__(self):
        return f"{self.wallet}"
