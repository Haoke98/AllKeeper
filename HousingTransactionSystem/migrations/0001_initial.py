# Generated by Django 3.2.7 on 2021-10-07 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HouseLayout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_created=True, auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updatedAt', models.DateTimeField(auto_now=True, null=True, verbose_name='最近更新时间')),
                ('deletedAt', models.DateTimeField(editable=False, null=True, verbose_name='被删除时间')),
                ('bedRoomCount', models.IntegerField(verbose_name='卧室（个数）')),
                ('livingRoomCount', models.IntegerField(verbose_name='客厅（个数）')),
                ('toiletCount', models.IntegerField(default=1, verbose_name='卫生间(个数)')),
                ('courtyardCount', models.IntegerField(default=0, verbose_name='院子（个数）')),
            ],
            options={
                'ordering': ['-updatedAt'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HousePriceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_created=True, auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updatedAt', models.DateTimeField(auto_now=True, null=True, verbose_name='最近更新时间')),
                ('deletedAt', models.DateTimeField(editable=False, null=True, verbose_name='被删除时间')),
                ('name', models.CharField(max_length=100, verbose_name='类型名')),
                ('unit', models.CharField(max_length=50, verbose_name='单位')),
            ],
            options={
                'ordering': ['-updatedAt'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HouseSizeUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_created=True, auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updatedAt', models.DateTimeField(auto_now=True, null=True, verbose_name='最近更新时间')),
                ('deletedAt', models.DateTimeField(editable=False, null=True, verbose_name='被删除时间')),
                ('name', models.CharField(max_length=50, verbose_name='单位称呼')),
                ('unit', models.CharField(max_length=50, verbose_name='单位符号')),
            ],
            options={
                'ordering': ['-updatedAt'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HouseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_created=True, auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updatedAt', models.DateTimeField(auto_now=True, null=True, verbose_name='最近更新时间')),
                ('deletedAt', models.DateTimeField(editable=False, null=True, verbose_name='被删除时间')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['-updatedAt'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_created=True, auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updatedAt', models.DateTimeField(auto_now=True, null=True, verbose_name='最近更新时间')),
                ('deletedAt', models.DateTimeField(editable=False, null=True, verbose_name='被删除时间')),
                ('owner', models.CharField(blank=True, max_length=100, verbose_name='电话号拥有者姓名')),
                ('number', models.BigIntegerField(verbose_name='联系电话')),
            ],
            options={
                'ordering': ['-updatedAt'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HouseSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_created=True, auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updatedAt', models.DateTimeField(auto_now=True, null=True, verbose_name='最近更新时间')),
                ('deletedAt', models.DateTimeField(editable=False, null=True, verbose_name='被删除时间')),
                ('size', models.FloatField(verbose_name='数字大小')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HousingTransactionSystem.housesizeunit', verbose_name='单位')),
            ],
            options={
                'ordering': ['-updatedAt'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HousePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_created=True, auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updatedAt', models.DateTimeField(auto_now=True, null=True, verbose_name='最近更新时间')),
                ('deletedAt', models.DateTimeField(editable=False, null=True, verbose_name='被删除时间')),
                ('price', models.IntegerField(verbose_name='价格（万）')),
                ('priceType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='HousingTransactionSystem.housepricetype')),
            ],
            options={
                'ordering': ['-updatedAt'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_created=True, auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updatedAt', models.DateTimeField(auto_now=True, null=True, verbose_name='最近更新时间')),
                ('deletedAt', models.DateTimeField(editable=False, null=True, verbose_name='被删除时间')),
                ('show_times', models.IntegerField(default=0, editable=False, verbose_name='被观看次数')),
                ('address', models.TextField()),
                ('descriptions', models.TextField()),
                ('images', models.TextField(null=True, verbose_name='所有图片的url和media_id')),
                ('houseLayout', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='HousingTransactionSystem.houselayout')),
                ('houseType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HousingTransactionSystem.housetype')),
                ('phoneNum', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='HousingTransactionSystem.phonenumber')),
                ('price', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='HousingTransactionSystem.houseprice')),
                ('size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='HousingTransactionSystem.housesize', verbose_name='占地面积')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
