# Generated by Django 4.2.7 on 2024-02-10 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_alter_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='meta_description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='توضیحات'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='کلمات کلیدی'),
        ),
    ]
