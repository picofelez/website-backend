from django.db import models
from django.utils import timezone

from account.models import User

# Create your models here.
from cart.models import Order


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


class AccessibilityChoices(models.TextChoices):
    private = 'p', 'خصوصی'
    customer = 'c', 'مشتری'


class Project(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام پروژه')
    description = models.TextField(verbose_name='توضیحات پروژه')
    customers = models.ManyToManyField(
        User, related_name='metallurgy_projects_user', verbose_name='مشتریان'
    )
    start_date = models.DateField(null=True, blank=True, verbose_name='تاریخ شروع پروژه')
    end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان پروژه')
    metal_orders = models.ManyToManyField(
        Order, blank=True, related_name='metallurgy_projects_order', verbose_name='سفارشات آهن'
    )
    accessibility_status = models.CharField(
        max_length=20, choices=AccessibilityChoices.choices, verbose_name='وضعیت دسترسی'
    )
    is_paid = models.BooleanField(default=False, verbose_name='وضعیت تسویه')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین ویرایش')

    class Meta:
        verbose_name = 'پروژه'
        verbose_name_plural = '3. پروژه ها'

    def get_total_expenses(self):
        total = 0
        for factor in self.invoices.all():
            total += factor.get_total_invoice_price()
        return f"{total:,}"

    get_total_expenses.short_description = 'مجموع فاکتور ها'

    def get_total_expenses_paid(self):
        total = 0
        for factor in self.invoices.filter(is_paid=True).all():
            total += factor.get_total_invoice_price()
        return f"{total:,}"

    get_total_expenses_paid.short_description = 'مجموع فاکتور های پرداخت شده'

    def __str__(self):
        return f"{self.name}"


class Invoice(models.Model):
    date = models.DateField(null=True, blank=True, verbose_name='تاریخ')
    project = models.ForeignKey(
        Project,
        related_name='invoices',
        on_delete=models.CASCADE,
        verbose_name='پروژه',
        null=True,
        blank=True
    )
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name='توضیح')
    is_paid = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    accessibility_status = models.CharField(
        max_length=20, choices=AccessibilityChoices.choices, verbose_name='وضعیت دسترسی'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'فاکتور'
        verbose_name_plural = '4. فاکتور ها'

    def get_total_invoice_price(self):
        total = 0
        for invoice_detail in self.invoice_details.all():
            total += invoice_detail.get_total_price()
        return total

    def __str__(self):
        return f"{self.project.name} | {self.get_total_invoice_price():,} تومان"


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name='invoice_details', verbose_name='فاکتور'
    )
    name = models.CharField(max_length=75, verbose_name='نام')
    quantity = models.BigIntegerField(default=1, verbose_name='مقدار')
    amount = models.BigIntegerField(verbose_name='قیمت')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'جزئیات فاکتور'
        verbose_name_plural = '5. جزئیات فاکتور'

    def get_total_price(self):
        return self.quantity * self.amount

    def __str__(self):
        return f"{self.get_total_price():,} تومان"
