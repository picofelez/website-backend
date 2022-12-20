# Generated by Django 4.1.4 on 2022-12-20 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import extensions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=155, verbose_name='نام نمایشی فروشگاه')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='شناسه اسلاگ')),
                ('image', models.ImageField(upload_to=extensions.upload_shop_image_path, verbose_name='تصویر')),
                ('location', models.CharField(max_length=100, verbose_name='مکان')),
                ('status', models.CharField(choices=[('a', 'فعال'), ('da', 'غیرفعال'), ('b', 'بلاک شده'), ('s', 'اسپم')], default='a', max_length=4, verbose_name='وضعیت فروشگاه')),
                ('about', models.TextField(verbose_name='متن دباره ما')),
                ('is_special', models.BooleanField(blank=True, default=False, null=True, verbose_name='برگزیده')),
                ('is_special_date', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ برگزیده شدن')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shops', to=settings.AUTH_USER_MODEL, verbose_name='مدیر فروشگاه')),
            ],
            options={
                'verbose_name': 'فروشگاه',
                'verbose_name_plural': '1. فروشگاه ها',
            },
        ),
    ]
