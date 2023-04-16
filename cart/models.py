from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from extensions.utils import generate_order_id, jalali_converter_dict
from product.models import Product
from shop.models import Shop

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
        verbose_name_plural = '5. آدرس ها'
        ordering = ('-created',)

    def __str__(self):
        return f"{self.name} | {self.city}"


class Order(models.Model):
    id = models.CharField(
        max_length=255, default=generate_order_id, primary_key=True, editable=False, unique=True
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='orders', verbose_name='کاربر'
    )
    address = models.ForeignKey(
        Address, on_delete=models.PROTECT, null=True, blank=True, verbose_name='آدرس'
    )
    message = models.TextField(null=True, blank=True, verbose_name='پیام')
    is_paid = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = '1. سفارشات'
        ordering = ('-created',)

    def total_order_detail_price(self):
        total = 0
        for order_detail in self.order_details.filter(is_confirmed=True):
            total += order_detail.total_price()

        return total

    total_order_detail_price.short_description = 'مجموع سبد خرید'

    def total_transportation_expense(self):
        total = 0
        for transfer in self.order_transfers.filter(status__in=['confirmed', 'posted']):
            total += transfer.expense

        return total

    total_transportation_expense.short_description = 'هزینه حمل و نقل'

    def amount_payable(self):
        return self.total_transportation_expense() + self.total_order_detail_price()

    amount_payable.short_description = 'مبلغ قابل پرداخت'

    def created_jalali(self):
        return jalali_converter_dict(self.created)

    def __str__(self):
        return f"سفارش : {self.user} - شناسه : {self.id}"


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_details', verbose_name='سفارش'
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, verbose_name='محصول'
    )
    count = models.IntegerField(default=1, verbose_name='تعداد')
    price = models.BigIntegerField(verbose_name='قیمت در زمان خرید')
    is_confirmed = models.BooleanField(default=True, verbose_name='تائید شده/نشده')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name = 'محصول در سفارش'
        verbose_name_plural = '4. محصولات در سفارش'

    def total_price(self):
        return self.price * self.count

    def __str__(self):
        return f"{self.product} - {self.order}"


class Transportation(models.Model):
    class StatusChoices(models.TextChoices):
        posted = 'posted', 'ارسال شده'
        pending = 'pending', 'درحال بررسی'
        returned = 'returned', 'برگشت خورده'
        confirmed = 'confirmed', 'تائید شده'

    shop = models.ForeignKey(
        Shop, on_delete=models.PROTECT, related_name='transportations', verbose_name='فروشگاه'
    )
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='order_transfers', verbose_name='سفارش'
    )
    expense = models.BigIntegerField(null=True, blank=True, verbose_name='هزینه حمل و نقل')
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.pending, verbose_name='وضعیت'
    )

    def transfer_total_price(self):
        price = 0
        for order_detail in self.order.order_details.all():
            if order_detail.product.shop == self.shop:
                price += order_detail.total_price()

        return price

    def transfer_final_price(self):
        if self.expense:
            return self.transfer_total_price() + self.expense

    class Meta:
        verbose_name = 'حمل و نقل'
        verbose_name_plural = '2. حمل و نقل ها'
        ordering = ('-id',)

    def __str__(self):
        return f"{self.order} | وضعیت : {self.status}"
