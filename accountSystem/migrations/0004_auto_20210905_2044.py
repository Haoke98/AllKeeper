# Generated by Django 3.2.6 on 2021-09-05 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0003_account_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': '账号', 'verbose_name_plural': '所有账号'},
        ),
        migrations.AlterModelOptions(
            name='accounttype',
            options={'verbose_name': '账号类型', 'verbose_name_plural': '所有账号类型'},
        ),
    ]