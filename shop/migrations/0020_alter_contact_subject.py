# Generated by Django 4.2.7 on 2023-11-20 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_alter_shop_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='subject',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='موضوع'),
        ),
    ]