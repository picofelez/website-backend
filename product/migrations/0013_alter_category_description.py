# Generated by Django 4.2.7 on 2024-02-09 12:17

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_category_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
    ]
