# Generated by Django 4.0 on 2022-01-16 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0034_alter_server_rootpwd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='ip',
            field=models.GenericIPAddressField(unique=True),
        ),
        migrations.CreateModel(
            name='ServerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_created=True, auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updatedAt', models.DateTimeField(auto_now=True, null=True, verbose_name='最近更新时间')),
                ('deletedAt', models.DateTimeField(editable=False, null=True, verbose_name='被删除时间')),
                ('username', models.CharField(max_length=32, null=True, verbose_name='用户名')),
                ('password', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accountSystem.password', verbose_name='密码')),
            ],
            options={
                'ordering': ['-updatedAt'],
                'abstract': False,
            },
        ),
    ]
