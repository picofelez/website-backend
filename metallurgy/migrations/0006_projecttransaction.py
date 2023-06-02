# Generated by Django 4.1.4 on 2023-04-25 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metallurgy', '0005_alter_project_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=255, verbose_name='خلاصه')),
                ('description', models.TextField(verbose_name='توضیحات تراکنش')),
                ('date', models.DateField(blank=True, null=True, verbose_name='تاریخ')),
                ('status', models.CharField(choices=[('s', 'موفق'), ('uns', 'ناموفق'), ('awp', 'دراننتظار پرداخت')], max_length=10, verbose_name='وضعیت پرداخت')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'تراکنش',
                'verbose_name_plural': '6. تراکنش های پروژه',
            },
        ),
    ]