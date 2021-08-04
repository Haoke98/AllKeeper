from django import forms
from django.db import models
# Create your models here.
from django.forms import TextInput
from django.template import loader
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .image import Image
from .base import MyModel
from miniProgram.utils import getVideoInfo


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


class ArticleAnalyseInput(TextInput):
    template_name = "ananlyse/article_analyse.html"

    def render(self, name, value, attrs=None, renderer=None):
        print("this is render:", self, name, value, attrs, renderer)
        context = self.get_context(name, value, attrs)
        context['widget']['value'] = value
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


from django.forms import ModelForm


class UploadForm(ModelForm):
    # url = forms.FileField(label="@Sadam图片", widget=ImageInput, help_text="按住ctrl进行多选,最多9张", required=False)

    class Meta:
        model = Image
        fields = ['content', 'media_id', 'url']


class ModelWithShowRate(MyModel):
    showTimes = models.IntegerField(verbose_name="被观看次数", default=0, editable=False)

    def show(self):
        self.showTimes += 1
        self.save()

    class Meta:
        abstract = True


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


class FilmType(ModelWithShowRate):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="标签名", max_length=50)
    unit = models.CharField(verbose_name="单位", max_length=50)

    def __str__(self):
        return "<%s,%s>" % (self.name, self.unit)


class Text(MyModel):
    id = models.AutoField(primary_key=True)
    english_text = models.CharField(max_length=100, verbose_name="英语_值", blank=True)
    uyghur_text = models.CharField(max_length=100, verbose_name="维吾尔语_值", blank=True)
    chinese_text = models.CharField(max_length=100, verbose_name="汉语_值", blank=True)

    def __str__(self):
        return "<%s,%s,%s>" % (self.english_text, self.uyghur_text, self.chinese_text)


class Language(MyModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="语言")
    symbol = models.CharField(max_length=100, verbose_name="符号")

    def __str__(self):
        return "<%s,%s>" % (self.name, self.symbol)


class Country(MyModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="国家")
    symbol = models.CharField(max_length=100, verbose_name="符号")

    def __str__(self):
        return "<%s,%s>" % (self.name, self.symbol)


class Film(ModelWithShowRate):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='电影标题', max_length=100)
    nameChinese = models.CharField(verbose_name="电影标题（中文）", max_length=100, blank=True, null=True)
    cover = models.ForeignKey(to=Image, on_delete=models.DO_NOTHING, null=True)
    type = models.ForeignKey(to=FilmType, on_delete=models.CASCADE, default=1)
    language = models.ForeignKey(to=Language, on_delete=models.CASCADE, default=1)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    def json(self, withEpisodes):
        json_object = {'film_id': self.id, 'name': self.name, 'cover': self.cover.url}
        if withEpisodes:
            episodes = Video.objects.filter(belongTo=self).order_by('-episodeNum', '-last_changed_time')
            episodes_list = []
            # episodes_dic = {}
            for per_episode in episodes:
                episodes_list.append(per_episode.json(False))
                # episodes_dic.setdefault(per_episode.id, per_episode.json())
            json_object["episodes"] = episodes_list
            # json_object["latest_episode_id"] = episodes[0].id
        else:
            pass
        return json_object

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # print("this Film :%s has been updated now. force_insert:%s force_update:%s," % (
        #     self.name, force_insert, force_update), using, update_fields)
        return super(Film, self).save(force_update=force_update, force_insert=force_insert, using=using,
                                      update_fields=update_fields)

    def show(self):
        self.type.show()
        super(Film, self).show()

    showTimes = models.IntegerField(verbose_name="被观看次数", default=0, )


class FilmForm(ModelForm):
    article_analyse = forms.CharField(label="公众号文章解析：", widget=ArticleAnalyseInput, help_text="这是一个悬浮窗口",
                                      required=False)

    class Meta:
        model = Film
        fields = ['name', 'nameChinese', 'cover', 'type', 'language', 'country']


class Video(ModelWithShowRate):
    id = models.AutoField(primary_key=True)
    episodeNum = models.IntegerField(verbose_name='集次', null=True, default=0)
    cover = models.ForeignKey(to=Image, on_delete=models.DO_NOTHING, blank=True, null=False, default=4)
    url = models.URLField(verbose_name='公众号文章链接', default="视频不见了的视频的链接", blank=True)
    belongTo = models.ForeignKey(verbose_name="所属电视剧", to=Film, on_delete=models.PROTECT, null=True)
    vid = models.CharField(verbose_name="vid", max_length=23, default=None, blank=True, null=True)

    def show(self):
        super(Video, self).show()

    # hasAnalysed = models.BooleanField(verbose_name="已经解析过", default=False)
    # TXVid = models.CharField(verbose_name="腾讯视频ID", max_length=11, default=None, blank=True)
    # isFromSubscription = models.BooleanField(verbose_name="来自公众号文章（需要解析）", default=True)
    # hasFirstAnalysed = models.BooleanField(verbose_name="已经进行过首次解析", default=False)
    # isTXV = models.BooleanField(verbose_name="是腾讯视频", default=False)

    # formatID = models.CharField(verbose_name="视频编码ID(决定视频流清晰度)", max_length=5, default="10002", blank=True, null=True)
    # destinationID = models.CharField(verbose_name="视频临时连接中的不变头部", max_length=36, default=None, blank=True, null=True)
    # analysedUrl = models.CharField(verbose_name="解析后的临时URL(有有效期)", max_length=400, default="#", blank=True, null=True)
    # analysedUrl_ExpiredTime = models.DateTimeField(verbose_name="解析后URL的过期DDL", auto_now_add=True)

    # def getAnalysedURL(self):
    #     if self.isTXV:
    #         return ""
    #     else:
    #         if not self.hasFirstAnalysed:
    #             self.analyse()
    #         if self.analysedUrl_ExpiredTime > timezone.now():
    #             print("this video:%s analysedURL has not been expired now." % self.name)
    #             return self.analysedUrl
    #         else:
    #             print("this video:%s analysedURL has been expired." % self.name)
    #             self.analysedUrl = analyseArticleUrl2(self.url, self.WXVid, self.formatID, self.destinationID)
    #             self.setExpiredTime()
    #             self.save()
    #             return self.analysedUrl

    # def getAnalysedURL(self):
    #     if self.analysedUrl_ExpiredTime > timezone.now():
    #         print("this video:%s analysedURL has not been expired now." % (self.name))
    #         return self.analysedUrl
    #     else:
    #         print("this video:%s analysedURL has been expired." % (self.name))
    #         if self.hasAnalysed:
    #             if self.isTXV:
    #                 self.analysedUrl = getTXVOriginalUrl(self.txvid)
    #             else:
    #                 self.isTXV, self.analysedUrl = analyseArticleUrl(url=self.url)
    #         else:
    #             self.isTXV, originalUrl_or_TXVid = analyseArticleUrl(url=self.url)
    #             if self.isTXV:
    #                 self.txvid = originalUrl_or_TXVid
    #                 self.analysedUrl = getTXVOriginalUrl(self.txvid)
    #             else:
    #                 self.analysedUrl = originalUrl_or_TXVid
    #             self.hasAnalysed = True
    #         self.setExpiredTime()
    #         self.save()
    #         return self.analysedUrl

    # def setExpiredTime(self):
    #     now = timezone.now()
    #     newHour = now.hour
    #     newDay = now.day
    #     newMonth = now.month
    #     newYear = now.year
    #     if newHour > 23:
    #         newDay += 1
    #         newHour -= 23
    #         if newMonth in [1, 3, 5, 7, 8, 10, 11]:
    #             if newDay > 31:
    #                 newMonth += 1
    #                 newDay -= 31
    #         else:
    #             if newDay > 30:
    #                 newMonth += 1
    #                 newDay -= 30
    #         if newMonth > 12:
    #             newYear += 1
    #             newMonth -= 12
    #     newDatetime = datetime(year=newYear, month=newMonth, day=newDay, hour=newHour,
    #                            minute=now.minute,
    #                            second=now.second, tzinfo=now.tzinfo)
    #     self.analysedUrl_ExpiredTime = newDatetime

    # def analyse(self):
    #     print("正在对视频进行提前解析：%s" % self.name)
    #     self.isTXV, Vid, _id, formatID, tempURl = analyseArticleUrl(self.url)
    #     if self.isTXV:
    #         self.TXVid = Vid
    #     else:
    #         self.WXVid = Vid
    #         self.destinationID = _id
    #         self.formatID = formatID
    #         self.analysedUrl = tempURl
    #         self.setExpiredTime()
    #     self.hasAnalysed = True
    #     self.hasFirstAnalysed = True
    #     self.save()
    def getPureVideoUrl(self):
        videoInfo = getVideoInfo(self.vid)
        # print("this is getPureVideoUrl:", videoInfo)
        original_url = videoInfo['url_info'][0]['url']
        return original_url

    def isTXV(self):
        return "wxv_" not in self.vid

    def __str__(self):
        return format_html("{}{}", self.belongTo, self.episode_name())

    def episode_name(self):
        if self.episodeNum == 0:
            return ""
        else:
            a = format_html("؛{}-{}", self.episodeNum, self.belongTo.type.unit)
            return a

    def json(self, isForSlider):
        if "wxv_" in self.vid:
            self.isTXV = False
        else:
            self.isTXV = True
        if isForSlider:
            cover = self.cover.url
        else:
            cover = self.belongTo.cover.url

        return {'vid': self.id, 'film_id': self.belongTo.id, 'name': self.episode_name(),
                'cover': cover,
                'isTXV': self.isTXV, 'TXVid': self.vid, 'url': self.url,
                'video_url': "https://x.izbasarweb.xyz/miniProgram/videoUrlVid=%d" % self.id}

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # print("this Video :%s has been saved now. force_insert:%s force_update:%s," % (
        #     self.__str__(), force_insert, force_update), using, update_fields)
        # if self.isFromSubscription:
        #     if not self.hasFirstAnalysed:
        #         self.analyse()
        #     if not self.hasAnalysed:
        #         self.getAnalysedURL()
        # else:
        #     pass
        # self.belongTo.save(force_update=True)
        return super(Video, self).save(force_update=force_update, force_insert=force_insert, using=using,
                                       update_fields=update_fields)


class VideoForm(ModelForm):
    # article_analyse = forms.CharField(label="公众号文章解析：", widget=ArticleAnalyseInput, help_text="请在这里输入，公众号文章链接",
    #                                   required=False)

    class Meta:
        model = Video
        fields = ['episodeNum', 'url', 'belongTo', 'vid']


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
