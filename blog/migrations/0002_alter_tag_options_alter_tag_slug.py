# Generated by Django 4.1.4 on 2023-01-29 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'برچسب', 'verbose_name_plural': '1. برچسب ها'},
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='شناسه'),
        ),
    ]
