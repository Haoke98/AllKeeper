# Generated by Django 4.0 on 2022-01-17 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0040_alter_bt_options_bt_path_alter_bt_basicauthpassword_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bt',
            name='path',
            field=models.SlugField(blank=True, null=True, verbose_name='面板路径'),
        ),
    ]
