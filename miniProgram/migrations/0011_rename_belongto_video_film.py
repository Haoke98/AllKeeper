# Generated by Django 3.2.6 on 2021-09-05 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miniProgram', '0010_alter_video_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='belongTo',
            new_name='film',
        ),
    ]
