# Generated by Django 4.0 on 2022-03-02 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0065_remove_dbserver_rootpwd_dbserver_pwd_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DbServer',
            new_name='DbService',
        ),
    ]