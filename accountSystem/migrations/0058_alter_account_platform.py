# Generated by Django 4.0 on 2022-02-04 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accountSystem', '0057_alter_account_platform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='platform',
            field=models.ForeignKey(limit_choices_to=models.Q(('url__isnull', False)), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='platform', to='accountSystem.type', verbose_name='所属平台'),
        ),
    ]
