from django import forms
from django.db import models
from django.forms import TextInput, ModelForm
from django.template import loader
from django.utils import timezone
from django.utils.safestring import mark_safe

from .base import MyModel, ModelWithShowRate
from .image import Image
from .video import Video


# Create your models here.


class ImageInput(TextInput):
    separator_media_id_src = "----"
    separator_images_info = "|||||"
    template_name = "upload_multi_img/image_multi_upload.html"

    def render(self, name, value, attrs=None, renderer=None):
        print("this is render:", self, name, value, attrs, renderer)
        context = self.get_context(name, value, attrs)
        context['widget']['value'] = value
        context['widget']['separator_media_id_src'] = self.separator_media_id_src
        context['widget']['separator_images_info'] = self.separator_images_info
        print("this is context on it :", context)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class RedirectUrlRelation(MyModel):
    name = models.CharField(max_length=50, null=True)
    id = models.IntegerField(primary_key=True)
    redirectUrl = models.CharField(max_length=500)
    returnValue = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "%s(URL重定向关系)" % (self.name)


class User(MyModel):
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


class Text(MyModel):
    id = models.AutoField(primary_key=True)
    english_text = models.CharField(max_length=100, verbose_name="英语_值", blank=True)
    uyghur_text = models.CharField(max_length=100, verbose_name="维吾尔语_值", blank=True)
    chinese_text = models.CharField(max_length=100, verbose_name="汉语_值", blank=True)

    def __str__(self):
        return "<%s,%s,%s>" % (self.english_text, self.uyghur_text, self.chinese_text)


class HouseType(MyModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class HouseLayout(MyModel):
    bedRoomCount = models.IntegerField(verbose_name="卧室（个数）")
    livingRoomCount = models.IntegerField(verbose_name="客厅（个数）")
    toiletCount = models.IntegerField(verbose_name="卫生间(个数)", default=1)
    courtyardCount = models.IntegerField(verbose_name="院子（个数）", default=0)

    def __str__(self):
        res = "户型："
        res += "%d室%d厅%d卫%d院" % (self.bedRoomCount, self.livingRoomCount, self.toiletCount, self.courtyardCount)
        return res


class PhoneNumber(MyModel):
    owner = models.CharField(max_length=100, verbose_name="电话号拥有者姓名", blank=True)
    number = models.BigIntegerField(verbose_name="联系电话", )

    def __str__(self):
        return "%d<%s>" % (self.number, self.owner)

    def json(self):
        return "TEL:%s" % (self.__str__())


class HousePriceType(MyModel):
    name = models.CharField(max_length=100, verbose_name="类型名")
    unit = models.CharField(max_length=50, verbose_name="单位")

    def __str__(self):
        return "<%s,%s>" % (self.name, self.unit)


class HousePrice(MyModel):
    priceType = models.ForeignKey(to=HousePriceType, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(verbose_name="价格（万）")

    def __str__(self):
        return "%s:%s%s" % (self.priceType.name, self.price, self.priceType.unit)


class HouseSizeUnit(MyModel):
    name = models.CharField(max_length=50, verbose_name="单位称呼")
    unit = models.CharField(max_length=50, verbose_name="单位符号")

    def __str__(self):
        return "<%s,%s>" % (self.name, self.unit)


class HouseSize(MyModel):
    size = models.FloatField(verbose_name="数字大小")
    unit = models.ForeignKey(to=HouseSizeUnit, on_delete=models.CASCADE, verbose_name="单位")

    def __str__(self):
        return "%0.2f%s" % (self.size, self.unit.__str__())


class House(ModelWithShowRate):
    houseType = models.ForeignKey(to=HouseType, on_delete=models.CASCADE)
    houseLayout = models.ForeignKey(to=HouseLayout, on_delete=models.CASCADE, null=True)
    # size = models.FloatField(verbose_name="占地面积(m2)", default=103)
    size = models.ForeignKey(to=HouseSize, on_delete=models.CASCADE, verbose_name="占地面积", null=True)
    price = models.ForeignKey(to=HousePrice, on_delete=models.CASCADE, null=True)
    phoneNum = models.ForeignKey(to=PhoneNumber, on_delete=models.CASCADE, null=True)
    address = models.TextField()
    descriptions = models.TextField()
    images = models.TextField(verbose_name="所有图片的url和media_id", null=True)

    def json(self):
        images_list = self.get_images_list()
        return {'houseType': self.houseType.__str__(), 'houseLayout': self.houseLayout.__str__(),
                'address': "地址：%s" % self.address,
                'descriptions': self.descriptions,
                'phoneNum': self.phoneNum.json(), 'size': "面积：%s" % self.size.__str__(),
                'price': self.price.__str__(), 'images': images_list}

    def get_images_list(self):

        text = self.images
        if text is None:
            list = []
        else:
            list = text.split(ImageInput.separator_images_info)
            res = []
            for i in list:
                res.append(i.split(ImageInput.separator_media_id_src)[1])
            list = res
        print(self, list)
        return list


class HouseForm(ModelForm):
    images = forms.CharField(label="@Sadam图片", widget=ImageInput, help_text="按住ctrl进行多选,最多9张", required=False)

    class Meta:
        model = House
        fields = ['houseType', 'houseLayout', 'size', 'price', 'phoneNum', 'address', 'descriptions', 'images']


class Subcribtions(MyModel):
    name = models.CharField(max_length=50)
    app_id = models.CharField(max_length=18)
    app_secret = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Settings(MyModel):
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


class StaticFiles(MyModel):
    label = models.CharField(verbose_name="文件标签", max_length=50, null=False)
    file = models.FileField(upload_to="static", null=False)
