# Generated by Django 3.2.6 on 2021-09-05 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniProgram', '0008_alter_filmtype_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='is_hot',
            field=models.BooleanField(blank=True, default=False, verbose_name='是否被推'),
        ),
    ]