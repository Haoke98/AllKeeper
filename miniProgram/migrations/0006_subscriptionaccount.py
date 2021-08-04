# Generated by Django 3.2.5 on 2021-08-03 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniProgram', '0005_auto_20210404_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('name', models.CharField(max_length=50)),
                ('appId', models.CharField(max_length=18)),
                ('appSecret', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
    ]