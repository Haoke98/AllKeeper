# Generated by Django 4.0 on 2022-01-15 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0032_remove_server_test2_alter_server_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accountSystem.group', verbose_name='所属账号组'),
        ),
    ]