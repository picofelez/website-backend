# Generated by Django 4.1.4 on 2023-07-10 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_shopinvoice_seen_shopscorehistory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shop',
            options={'ordering': ('-score',), 'verbose_name': 'فروشگاه', 'verbose_name_plural': '1. فروشگاه ها'},
        ),
    ]