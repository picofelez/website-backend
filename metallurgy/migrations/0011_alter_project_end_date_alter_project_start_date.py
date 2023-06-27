# Generated by Django 4.1.4 on 2023-06-27 17:20

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('metallurgy', '0010_alter_invoice_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ پایان پروژه'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ شروع پروژه'),
        ),
    ]