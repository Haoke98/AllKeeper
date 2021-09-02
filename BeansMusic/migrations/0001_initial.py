# Generated by Django 3.2.6 on 2021-09-02 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('date', models.DateTimeField(auto_created=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.FileField(upload_to='BeansMusicVideos')),
                ('likeCount', models.IntegerField(null=True)),
                ('commentCount', models.IntegerField(null=True)),
                ('shareCount', models.IntegerField(null=True)),
                ('title', models.CharField(max_length=100, null=True)),
                ('introduction', models.TextField(null=True)),
            ],
        ),
    ]
