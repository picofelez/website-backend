# Generated by Django 4.2.7 on 2023-12-23 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(default=100733, max_length=255, verbose_name='اسلاگ'),
        ),
    ]
