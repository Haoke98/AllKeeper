# Generated by Django 3.2.6 on 2021-09-02 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miniProgram', '0003_remove_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='showTimes',
            new_name='show_times',
        ),
        migrations.RenameField(
            model_name='film',
            old_name='showTimes',
            new_name='show_times',
        ),
        migrations.RenameField(
            model_name='filmtype',
            old_name='showTimes',
            new_name='show_times',
        ),
        migrations.RenameField(
            model_name='house',
            old_name='showTimes',
            new_name='show_times',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='showTimes',
            new_name='show_times',
        ),
    ]