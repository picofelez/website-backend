# Generated by Django 4.1.4 on 2023-06-25 07:48

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('metallurgy', '0009_invoicedetail_quantity_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ'),
        ),
    ]
