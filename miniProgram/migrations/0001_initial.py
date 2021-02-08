# Generated by Django 3.1.5 on 2021-01-31 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('showTimes', models.IntegerField(default=0, editable=False, verbose_name='被观看次数')),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=120)),
                ('cover_url', models.URLField()),
                ('url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='国家')),
                ('symbol', models.CharField(max_length=100, verbose_name='符号')),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='电影标题')),
                ('nameChinese', models.CharField(blank=True, max_length=100, null=True, verbose_name='电影标题（中文）')),
                ('showTimes', models.IntegerField(default=0, verbose_name='被观看次数')),
                ('country', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='miniProgram.country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FilmType',
            fields=[
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('showTimes', models.IntegerField(default=0, editable=False, verbose_name='被观看次数')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='标签名')),
                ('unit', models.CharField(max_length=50, verbose_name='单位')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HouseLayout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('bedRoomCount', models.IntegerField(verbose_name='卧室（个数）')),
                ('livingRoomCount', models.IntegerField(verbose_name='客厅（个数）')),
                ('toiletCount', models.IntegerField(default=1, verbose_name='卫生间(个数)')),
                ('courtyardCount', models.IntegerField(default=0, verbose_name='院子（个数）')),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HousePriceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('name', models.CharField(max_length=100, verbose_name='类型名')),
                ('unit', models.CharField(max_length=50, verbose_name='单位')),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HouseSizeUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('name', models.CharField(max_length=50, verbose_name='单位称呼')),
                ('unit', models.CharField(max_length=50, verbose_name='单位符号')),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HouseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('media_id', models.CharField(blank=True, default='#', max_length=43)),
                ('url', models.CharField(blank=True, default='#', max_length=500)),
                ('content', models.ImageField(blank=True, upload_to='img')),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='语言')),
                ('symbol', models.CharField(max_length=100, verbose_name='符号')),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('owner', models.CharField(blank=True, max_length=100, verbose_name='电话号拥有者姓名')),
                ('number', models.BigIntegerField(verbose_name='联系电话')),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RedirectUrlRelation',
            fields=[
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('name', models.CharField(max_length=50, null=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('redirectUrl', models.CharField(max_length=500)),
                ('returnValue', models.CharField(max_length=100, null=True)),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaticFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('label', models.CharField(max_length=50, verbose_name='文件标签')),
                ('file', models.FileField(upload_to='static')),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='subcribtions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('name', models.CharField(max_length=50)),
                ('app_id', models.CharField(max_length=18)),
                ('app_secret', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('english_text', models.CharField(blank=True, max_length=100, verbose_name='英语_值')),
                ('uyghur_text', models.CharField(blank=True, max_length=100, verbose_name='维吾尔语_值')),
                ('chinese_text', models.CharField(blank=True, max_length=100, verbose_name='汉语_值')),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('openid', models.CharField(max_length=44)),
                ('vip_expiredTime', models.DateTimeField(blank=True, null=True, verbose_name='VIP过期时间')),
                ('firstTimeLogin', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_login_time', models.DateTimeField(blank=True, null=True, verbose_name='最近一次登陆时间')),
                ('nickName', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.IntegerField(blank=True, null=True)),
                ('language', models.CharField(blank=True, max_length=5, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('province', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('avatarUrl', models.URLField(blank=True, null=True)),
                ('remark', models.CharField(blank=True, max_length=100, null=True)),
                ('systemInfo', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-last_login_time'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('showTimes', models.IntegerField(default=0, editable=False, verbose_name='被观看次数')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('episodeNum', models.IntegerField(default=0, null=True, verbose_name='集次')),
                ('url', models.URLField(blank=True, default='视频不见了的视频的链接', verbose_name='公众号文章链接')),
                ('vid', models.CharField(blank=True, default=None, max_length=23, null=True, verbose_name='vid')),
                ('belongTo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='miniProgram.film', verbose_name='所属电视剧')),
                ('cover', models.ForeignKey(blank=True, default=32, on_delete=django.db.models.deletion.DO_NOTHING, to='miniProgram.image')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('app_name', models.CharField(max_length=50)),
                ('app_id', models.CharField(max_length=18)),
                ('app_secret', models.CharField(max_length=32)),
                ('enableVIP_mode', models.BooleanField(verbose_name='是否启动VIP模式')),
                ('VIPprice', models.FloatField(null=True, verbose_name='一个月会员价')),
                ('trialTime', models.IntegerField(default=300, verbose_name='试看时间（秒）')),
                ('total_transaction_volume', models.FloatField(default=0, verbose_name='本平台总交易额')),
                ('sliders', models.ManyToManyField(to='miniProgram.Video')),
                ('subcribtion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='miniProgram.subcribtions')),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HouseSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('size', models.FloatField(verbose_name='数字大小')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miniProgram.housesizeunit', verbose_name='单位')),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HousePrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('price', models.IntegerField(verbose_name='价格（万）')),
                ('priceType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='miniProgram.housepricetype')),
            ],
            options={
                'ordering': ['-last_changed_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed_time', models.DateTimeField(auto_now=True, verbose_name='最近一次修改时间')),
                ('showTimes', models.IntegerField(default=0, editable=False, verbose_name='被观看次数')),
                ('address', models.TextField()),
                ('descriptions', models.TextField()),
                ('images', models.TextField(null=True, verbose_name='所有图片的url和media_id')),
                ('houseLayout', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='miniProgram.houselayout')),
                ('houseType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miniProgram.housetype')),
                ('phoneNum', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='miniProgram.phonenumber')),
                ('price', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='miniProgram.houseprice')),
                ('size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='miniProgram.housesize', verbose_name='占地面积')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='film',
            name='cover',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='miniProgram.image'),
        ),
        migrations.AddField(
            model_name='film',
            name='language',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='miniProgram.language'),
        ),
        migrations.AddField(
            model_name='film',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='miniProgram.filmtype'),
        ),
    ]
