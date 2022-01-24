# Generated by Django 4.0 on 2022-01-17 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0039_alter_account_options_bt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bt',
            options={'verbose_name': '宝塔', 'verbose_name_plural': '所有宝塔'},
        ),
        migrations.AddField(
            model_name='bt',
            name='path',
            field=models.URLField(blank=True, null=True, verbose_name='面板路径'),
        ),
        migrations.AlterField(
            model_name='bt',
            name='basicAuthPassword',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basicAuthPassword', to='accountSystem.password', verbose_name='BasicAuth密码'),
        ),
        migrations.AlterField(
            model_name='bt',
            name='basicAuthUsername',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='BasicAuth用户名'),
        ),
    ]