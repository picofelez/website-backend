# Generated by Django 4.1.4 on 2023-01-13 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11, verbose_name='شماره تلفن')),
                ('full_name', models.CharField(max_length=255, verbose_name='نام و نام خانوادگی')),
                ('national_code', models.CharField(max_length=10, verbose_name='کدملی')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sellers', to='shop.shop', verbose_name='فروشگاه')),
            ],
            options={
                'verbose_name': 'اطلاعات فروشنده',
                'verbose_name_plural': '3. اطلاعات فروشندگان',
            },
        ),
    ]
