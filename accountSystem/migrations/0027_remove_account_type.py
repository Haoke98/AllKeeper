# Generated by Django 4.0 on 2021-12-18 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0026_rename_typebeta_account_types'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='type',
        ),
    ]
