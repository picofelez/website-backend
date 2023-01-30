# Generated by Django 4.1.4 on 2023-01-30 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_delete_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('status', models.CharField(choices=[('a', 'فعال'), ('da', 'غیرفعال')], default='a', max_length=5, verbose_name='وضعیت نمایش')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
            ],
            options={
                'verbose_name': 'سوال',
                'verbose_name_plural': 'سوالات متداول',
            },
        ),
    ]
