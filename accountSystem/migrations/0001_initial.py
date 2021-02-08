# Generated by Django 3.1.5 on 2021-01-31 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Password',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('username', models.CharField(max_length=20, verbose_name='用户名')),
                ('password', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountSystem.password')),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
    ]
