# Generated by Django 3.1.6 on 2021-02-14 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniProgram', '0003_settings_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='enableVIP_mode',
            field=models.BooleanField(default=False, verbose_name='是否启动VIP模式'),
        ),
    ]