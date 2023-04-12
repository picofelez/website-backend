# Generated by Django 4.1.4 on 2023-04-12 22:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_order_message'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('metallurgy', '0002_alter_worksampleimage_options_alter_worksample_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='تاریخ')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='توضیح')),
                ('is_paid', models.BooleanField(default=False, verbose_name='وضعیت پرداخت')),
                ('accessibility_status', models.CharField(choices=[('p', 'خصوصی'), ('c', 'مشتری')], max_length=20, verbose_name='وضعیت دسترسی')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'فاکتور',
                'verbose_name_plural': '4. فاکتور ها',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام پروژه')),
                ('description', models.TextField(verbose_name='توضیحات پروژه')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='تاریخ شروع پروژه')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='تاریخ پایان پروژه')),
                ('accessibility_status', models.CharField(choices=[('p', 'خصوصی'), ('c', 'مشتری')], max_length=20, verbose_name='وضعیت دسترسی')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین ویرایش')),
                ('customers', models.ManyToManyField(related_name='metallurgy_projects_user', to=settings.AUTH_USER_MODEL, verbose_name='مشتریان')),
                ('metal_orders', models.ManyToManyField(blank=True, related_name='metallurgy_projects_order', to='cart.order', verbose_name='سفارشات آهن')),
            ],
            options={
                'verbose_name': 'پروژه',
                'verbose_name_plural': '3. پروژه ها',
            },
        ),
        migrations.CreateModel(
            name='InvoiceDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, verbose_name='نام')),
                ('quantity', models.BigIntegerField(default=1, verbose_name='مقدار')),
                ('amount', models.BigIntegerField(verbose_name='قیمت')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_details', to='metallurgy.invoice', verbose_name='فاکتور')),
            ],
            options={
                'verbose_name': 'جزئیات فاکتور',
                'verbose_name_plural': '5. جزئیات فاکتور ها',
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='metallurgy.project', verbose_name='پروژه'),
        ),
    ]
