from django.db import models

# Create your models here.
from django.utils import timezone


class MyModel(models.Model):
    last_changed_time = models.DateTimeField(verbose_name='最近一次修改时间', auto_now=True)

    class Meta:
        abstract = True

    # def save(self, *args, **kwargs):
    #     # self.last_changed_time =
    #     super().save(*args, **kwargs)


class Article(MyModel):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=120)
    cover_url = models.URLField()
    url = models.URLField()

    def __str__(self):
        return self.title

    def json(self):
        return {
            'title': self.title,
            'description': self.description,
            'cover_url': self.cover_url,
            'url': self.cover_url,
        }


class RedirectUrlRelation(MyModel):
    name = models.CharField(max_length=50, null=True)
    id = models.IntegerField(primary_key=True)
    redirectUrl = models.CharField(max_length=500)
    returnValue = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "%s(URL重定向关系)" % (self.name)


class User(MyModel):
    openid = models.CharField(max_length=44)
    vip_expiredTime = models.DateTimeField(verbose_name="VIP过期时间", null=True)
    firstTimeLogin = models.DateTimeField(auto_now_add=True, null=True)
    last_login_time = models.DateTimeField(verbose_name='最近一次登陆时间', null=True)
    nickName = models.CharField(max_length=100, null=True)
    gender = models.IntegerField(null=True)
    language = models.CharField(max_length=4, null=True)
    city = models.CharField(max_length=50, null=True)
    province = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    avatarUrl = models.URLField(null=True)

    def updateUserInfo(self, json_data):
        self.nickName = json_data['nickName']
        self.gender = json_data['gender']
        self.language = json_data['language']
        self.city = json_data['city']
        self.province = json_data['province']
        self.country = json_data['country']
        self.avatarUrl = json_data['avatarUrl']
        self.save()

    def __str__(self):
        return self.openid

    def json(self):
        isVIP = False
        now = timezone.now()
        dateTimeDelta = self.vip_expiredTime - now
        vipAlert = "VIPئەزارىمىزنى قىزغىن قارشى ئالىمىز"
        if dateTimeDelta.days == 0:
            vipAlert = "VIPئەزالىقىڭىزنىڭ ۋاقتى ئۆتىدىغانغا نەچچە سائەتلا ۋاقىت قالدى"
        else:
            if dateTimeDelta.days <= 15:
                vipAlert = "كۈنلا ۋاقىت قالدى" + str(dateTimeDelta.days) + "VIPئەزالىقىڭىز ۋاقتى ئۆتىدىغانغا يەنە "
                vipAlert = "VIPئەزالىقىڭىزنىڭ ۋاقتى پەقەت%dكۈنلا قالدى" % (dateTimeDelta.days)
        if now < self.vip_expiredTime:
            isVIP = True
        userJson = {
            "openid": self.openid,
            "isVIP": isVIP,
            "vipAlert": vipAlert
        }
        return userJson


class film(MyModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='电影标题', max_length=100)
    cover = models.URLField(verbose_name='电影封面',
                            default='https://mmbiz.qpic.cn/mmbiz_png/lBSHibv6GicCZ6TSPK91xVfqr0cGAiany3uOqL6lz3QvMMmGRdib5QaDxF6kN1JKIQRl4xVWH7yW2GIqn4J4ZdkE9A/0?wx_fmt=png',
                            blank=True)

    def __str__(self):
        return self.name


class video(MyModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='每一集的名字', max_length=50)
    episode_num = models.IntegerField(verbose_name='集次', null=True)
    cover = models.URLField(verbose_name='视频封面',
                            default='https://mmbiz.qpic.cn/mmbiz_png/lBSHibv6GicCZ6TSPK91xVfqr0cGAiany3u55miazzYxVibcryAlMdVrDyyoaJ7Qp7XmS7K5kIwTdtla9piaFInusjJA/0?wx_fmt=png',
                            blank=True)
    url = models.URLField(verbose_name='视频链接', default="视频不见了的视频的链接", blank=True)
    belongTo = models.ForeignKey(verbose_name="所属电视剧", to=film, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class subcribtions(MyModel):
    name = models.CharField(max_length=50)
    app_id = models.CharField(max_length=18)
    app_secret = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class settings(MyModel):
    app_name = models.CharField(max_length=50)
    app_id = models.CharField(max_length=18)
    app_secret = models.CharField(max_length=32)
    sliders = models.ManyToManyField(to=video)
    subcribtion = models.ForeignKey(to=subcribtions, on_delete=models.PROTECT, null=True)
    enableVIP_mode = models.BooleanField(verbose_name="是否启动VIP模式")
    VIPprice = models.FloatField(verbose_name="一个月会员价", null=True)

    def __str__(self):
        return self.app_name

    def json(self):
        return {
            "enableVIP_mode": self.enableVIP_mode,
            "VIPprice": self.VIPprice,
        }
