# Generated by Django 4.0 on 2022-02-01 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0047_alter_server_hoster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wechat',
            name='wx_id',
        ),
        migrations.AlterField(
            model_name='wechat',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]