# Generated by Django 4.0 on 2021-12-18 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0025_account_typebeta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='typeBeta',
            new_name='types',
        ),
    ]
