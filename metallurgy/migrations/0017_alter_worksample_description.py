# Generated by Django 4.2.7 on 2023-12-22 10:42

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metallurgy', '0016_worksample_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worksample',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='توضیحات'),
        ),
    ]