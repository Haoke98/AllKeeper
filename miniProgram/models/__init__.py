from django.db import models
from django.forms import ModelForm
from django.utils import timezone

from izBasar.models import BaseModel, ModelWithShowRate
from .base import *
from .image import *
from .image import Image
from .subscriptionAccountModel import *
from .video import Video


# Create your models here.


class RedirectUrlRelation(BaseModel):
    name = models.CharField(max_length=50, null=True)
    id = models.IntegerField(primary_key=True)
    redirectUrl = models.CharField(max_length=500)
    returnValue = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "%s(URL重定向关系)" % self.name


class User(BaseModel):
    openid = models.CharField(max_length=44)
    vip_expiredTime = models.DateTimeField(verbose_name="VIP过期时间", blank=True, null=True)
    firstTimeLogin = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_login_time = models.DateTimeField(verbose_name='最近一次登陆时间', blank=True, null=True)
    nickName = models.CharField(max_length=100, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    avatarUrl = models.URLField(blank=True, null=True)
    remark = models.CharField(null=True, blank=True, max_length=100)
    systemInfo = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "小程序用户"
        verbose_name_plural = "所有" + verbose_name
        ordering = ['-last_login_time']

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
            "vipAlert": vipAlert,
            "firstTimeLogin": self.firstTimeLogin.ctime(),
            "last_login_time": self.last_login_time.ctime(),
            "vip_expired_time": self.vip_expiredTime.ctime(),
            "nikName": self.nickName,
            "gender": self.gender,
            "language": self.language,
            "city": self.city,
            "province": self.province,
            "country": self.country,
            "avatarUrl": self.avatarUrl,
        }
        return userJson


class UploadForm(ModelForm):
    # url = forms.FileField(label="@Sadam图片", widget=ImageInput, help_text="按住ctrl进行多选,最多9张", required=False)

    class Meta:
        model = Image
        fields = ['content', 'media_id', 'original_url']


class Article(ModelWithShowRate):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=120)
    cover_url = models.URLField()
    url = models.URLField()

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     return super(Article,self).save(force_insert=force_insert,force_update=force_update,)
    def __str__(self):
        return self.title

    def json(self):
        return {
            'title': self.title,
            'description': self.description,
            'cover_url': self.cover_url,
            'url': self.url,
        }

    class Meta:
        verbose_name = "订阅号文章"
        verbose_name_plural = "所有" + verbose_name


class Text(BaseModel):
    id = models.AutoField(primary_key=True)
    english_text = models.CharField(max_length=100, verbose_name="英语_值", blank=True)
    uyghur_text = models.CharField(max_length=100, verbose_name="维吾尔语_值", blank=True)
    chinese_text = models.CharField(max_length=100, verbose_name="汉语_值", blank=True)

    def __str__(self):
        return "<%s,%s,%s>" % (self.english_text, self.uyghur_text, self.chinese_text)


class Subcribtions(BaseModel):
    name = models.CharField(max_length=50)
    app_id = models.CharField(max_length=18)
    app_secret = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Settings(BaseModel):
    app_name = models.CharField(max_length=50)
    app_id = models.CharField(max_length=18)
    app_secret = models.CharField(max_length=32)
    sliders = models.ManyToManyField(to=Video)
    subcribtion = models.ForeignKey(to=Subcribtions, on_delete=models.PROTECT, null=True)
    enableVIP_mode = models.BooleanField(verbose_name="是否启动VIP模式", default=False)
    VIPprice = models.FloatField(verbose_name="一个月会员价", null=True)
    trialTime = models.IntegerField(verbose_name="试看时间（秒）", default=5 * 60)
    total_transaction_volume = models.FloatField(verbose_name="本平台总交易额", default=0)
    host = models.URLField(verbose_name="服务器运行的地址", null=True, blank=True)

    def __str__(self):
        return self.app_name

    def json(self):
        return {
            "enableVIP_mode": self.enableVIP_mode,
            "VIPprice": self.VIPprice,
            "trialTime": self.trialTime,
        }


class StaticFiles(BaseModel):
    label = models.CharField(verbose_name="文件标签", max_length=50, null=False)
    file = models.FileField(upload_to="static", null=False)
