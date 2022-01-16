# Generated by Django 4.0 on 2022-01-16 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0036_serveruser_hasrootpriority'),
    ]

    operations = [
        migrations.AddField(
            model_name='serveruser',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accountSystem.group', verbose_name='所属个体/组织'),
        ),
        migrations.AddField(
            model_name='serveruser',
            name='server',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accountSystem.server', verbose_name='服务器'),
        ),
    ]
