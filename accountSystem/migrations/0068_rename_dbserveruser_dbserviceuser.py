# Generated by Django 4.0 on 2022-03-02 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0067_alter_dbserveruser_password'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DbServerUser',
            new_name='DbServiceUser',
        ),
    ]