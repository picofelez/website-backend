# Generated by Django 4.1.4 on 2023-07-03 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_alter_shopinvoice_options_shopinvoice_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopinvoice',
            name='title',
        ),
    ]
