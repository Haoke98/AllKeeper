# Generated by Django 4.0 on 2022-02-01 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0048_remove_wechat_wx_id_alter_wechat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechat',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='微信号（ID）'),
        ),
    ]
