# Generated by Django 3.1.6 on 2021-04-22 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0004_auto_20210422_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(default='未知账号', max_length=50, verbose_name='账号归属'),
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=50, verbose_name='用户名'),
        ),
    ]
