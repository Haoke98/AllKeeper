# Generated by Django 3.2.7 on 2021-10-05 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0011_alter_account_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='Introduce',
            new_name='info',
        ),
    ]
