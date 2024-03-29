import uuid

from django.db import models
from django.urls import reverse
from django.utils.html import format_html

from account.models import User
from extensions.utils import upload_shop_image_path, jalali_converter, generate_product_id
from .managers import ActiveShopManager, ShopInvoiceManager
from django_jalali.db import models as jmodels


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
    score = models.IntegerField(default=0, verbose_name='امتیاز')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name = 'فروشگاه'
        verbose_name_plural = '1. فروشگاه ها'
        ordering = ('-score',)

    objects = models.Manager()
    active = ActiveShopManager()

    def increase_score(self, increase_count, summary):
        self.score_histories.create(
            value=increase_count,
            summary=summary
        )
        self.score += increase_count
        self.save()

    def get_thumbnail(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 5px;' src='{self.image.url}'>")

    get_thumbnail.short_description = "تصویر فروشگاه"

    def get_absolute_url(self):
        return reverse('shop:shop-detail', args=[self.slug])

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
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name='موضوع')
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
    confirmed = models.BooleanField(default=False, verbose_name='تائید شده/نشده')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name_plural = '4. کیف پول ها'
        verbose_name = 'کیف پول'
        ordering = ('-created',)

    def created_jalali(self):
        return f"{jalali_converter(self.created)} ساعت {self.created.hour}:{self.created.minute}"

    created_jalali.short_description = 'تاریخ ایجاد'

    def updated_jalali(self):
        return f"{jalali_converter(self.updated)} ساعت {self.updated.hour}:{self.updated.minute}"

    updated_jalali.short_description = 'تاریخ آخرین ویرایش'

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


class ShopInvoice(models.Model):
    class InvoiceTypeChoices(models.TextChoices):
        pre_invoice = 'pre', 'پیش فاکتور'
        sales_invoice = 'sales', 'فاکتور فروش'

    id = models.CharField(
        max_length=255, default=generate_product_id, primary_key=True, editable=False, unique=True
    )
    shop = models.ForeignKey(
        Shop, on_delete=models.PROTECT, related_name='shop_invoices', verbose_name='فروشگاه'
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, related_name='order_invoices', verbose_name='خریدار'
    )
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='نشانی')
    date = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ')
    tax = models.BigIntegerField(default=0, verbose_name='مالیات')
    discount = models.BigIntegerField(default=0, verbose_name='تخفیف')
    transport_cost = models.BigIntegerField(default=0, verbose_name='کرایه باربری')
    invoice_shop = models.CharField(max_length=20, choices=InvoiceTypeChoices.choices, verbose_name='تایپ فاکتور')
    life_time = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ اعتبار')
    seen = models.BooleanField(default=False, verbose_name='مشاهده شده توسط مشتری')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name_plural = '6. فاکتور های فروشگاه'
        verbose_name = 'فاکتور فروشگاه'
        ordering = ('-created',)

    objects = ShopInvoiceManager()

    def get_total_invoice_details(self):
        total = 0
        for invoice_detail in self.invoice_details.select_related(None).all():
            total += invoice_detail.get_total_price()
        return total

    def get_total_invoice_price(self):
        tax_percent = int(((self.get_total_invoice_details() * self.tax) / 100) + self.get_total_invoice_details())
        return tax_percent - self.discount + self.transport_cost

    def get_total_details_display(self):
        return f"{self.get_total_invoice_details():,}"

    get_total_details_display.short_description = 'جمع خالص فاکتور'

    def get_total_price_display(self):
        return f"{self.get_total_invoice_price():,}"

    get_total_price_display.short_description = 'جمع کل فاکتور'

    def __str__(self):
        return f"{self.shop} - {self.get_total_invoice_details():,} - {self.get_total_invoice_price():,}"


class ShopInvoiceDetail(models.Model):
    invoice = models.ForeignKey(
        ShopInvoice, on_delete=models.CASCADE, related_name='invoice_details', verbose_name='فاکتور'
    )
    name = models.CharField(max_length=75, verbose_name='نام')
    quantity = models.BigIntegerField(default=1, verbose_name='مقدار')
    quantity_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='واحد')
    amount = models.BigIntegerField(verbose_name='قیمت')
    count_of_order = models.CharField(max_length=255, null=True, blank=True, verbose_name='تعداد')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '7. جزئیات فاکتور ها'
        verbose_name = 'جزئیات فاکتور'

    def get_total_price(self):
        return self.quantity * self.amount

    def get_total_price_display(self):
        return f"{self.get_total_price():,}"

    get_total_price_display.short_description = 'جمع'

    def __str__(self):
        return f"{self.get_total_price():,} تومان"


class ShopScoreHistory(models.Model):
    value = models.IntegerField(default=0, verbose_name='مقدار امتیاز')
    summary = models.CharField(max_length=255, verbose_name='دلیل امتیاز')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    shop = models.ForeignKey(
        Shop, on_delete=models.PROTECT, related_name='score_histories', verbose_name='برای فروشگاه'
    )

    class Meta:
        verbose_name = 'تاریخچه امتیاز'
        verbose_name_plural = '8. تاریخجه امتیازات'

    def __str__(self):
        return f"{self.shop.title} - {self.value} امتیاز"
