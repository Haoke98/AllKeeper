# Generated by Django 4.0 on 2022-02-27 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0061_alter_password_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElasticSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_created=True, auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updatedAt', models.DateTimeField(auto_now=True, null=True, verbose_name='最近更新时间')),
                ('deletedAt', models.DateTimeField(editable=False, null=True, verbose_name='被删除时间')),
                ('remark', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('port', models.PositiveIntegerField(default=8888, verbose_name='端口')),
                ('elasticPwd', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accountSystem.password', verbose_name='elastic')),
                ('server', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accountSystem.server', verbose_name='服务器')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]