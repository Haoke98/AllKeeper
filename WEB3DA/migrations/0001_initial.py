# Generated by Django 3.2.7 on 2021-10-07 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_created=True, auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updatedAt', models.DateTimeField(auto_now=True, null=True, verbose_name='最近更新时间')),
                ('deletedAt', models.DateTimeField(editable=False, null=True, verbose_name='被删除时间')),
                ('name', models.CharField(max_length=50, verbose_name='贴图名称')),
            ],
            options={
                'ordering': ['-updatedAt'],
                'abstract': False,
            },
        ),
    ]
