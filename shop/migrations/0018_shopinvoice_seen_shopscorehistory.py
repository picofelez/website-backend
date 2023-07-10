# Generated by Django 4.1.4 on 2023-07-10 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_shop_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopinvoice',
            name='seen',
            field=models.BooleanField(default=False, verbose_name='مشاهده شده توسط مشتری'),
        ),
        migrations.CreateModel(
            name='ShopScoreHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0, verbose_name='مقدار امتیاز')),
                ('summary', models.CharField(max_length=255, verbose_name='دلیل امتیاز')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='score_histories', to='shop.shop', verbose_name='برای فروشگاه')),
            ],
            options={
                'verbose_name': 'تاریخچه امتیاز',
                'verbose_name_plural': '8. تاریخجه امتیازات',
            },
        ),
    ]
