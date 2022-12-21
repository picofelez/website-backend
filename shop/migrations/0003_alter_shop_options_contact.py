# Generated by Django 4.1.4 on 2022-12-20 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_shop_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shop',
            options={'ordering': ('-created',), 'verbose_name': 'فروشگاه', 'verbose_name_plural': '1. فروشگاه ها'},
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')),
                ('subject', models.CharField(max_length=100, verbose_name='موضوع')),
                ('phone', models.CharField(max_length=12, verbose_name='شماره تلفن')),
                ('message', models.TextField(verbose_name='پیام')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='shop.shop', verbose_name='فروشگاه گیرنده')),
            ],
            options={
                'verbose_name': 'پیام',
                'verbose_name_plural': '2. پیام ها',
                'ordering': ('-created',),
            },
        ),
    ]