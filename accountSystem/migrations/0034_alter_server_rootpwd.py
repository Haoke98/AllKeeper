# Generated by Django 4.0 on 2022-01-15 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0033_server_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='rootPwd',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accountSystem.password', verbose_name='密码'),
        ),
    ]