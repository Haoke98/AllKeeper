import os
import urllib

import requests
from django.core.files import File
from django.db import models
# Create your models here.
from django.forms import ClearableFileInput
from django.template import loader
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from izBasar.settings import MEDIA_ROOT
from .utils import getVideoInfo


class ImageInput(ClearableFileInput):
    template_name = "upload_multi_img/image_multi_upload.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class MyModel(models.Model):
    last_changed_time = models.DateTimeField(verbose_name='最近一次修改时间', auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-last_changed_time']

    # def save(self, *args,**kwargs):
    #     self.last_changed_time =
    #     return super(MyModel,self).save(*args,**kwargs)
    # def save(self, *args, **kwargs):
    #     # self.last_changed_time =
    #     super().save(*args, **kwargs)


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
    language = models.CharField(max_length=5, null=True)
    city = models.CharField(max_length=50, null=True)
    province = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    avatarUrl = models.URLField(null=True)

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
            "vipAlert": vipAlert
        }
        return userJson


class Image(MyModel):
    id = models.AutoField(primary_key=True)
    media_id = models.CharField(max_length=43, blank=True, default="#")
    # url_default_choices = (("#", "#"),)
    # url = models.CharField(max_length=500, blank=True, default="#",choices=url_default_choices)
    url = models.CharField(max_length=500, blank=True, default="#")
    content = models.ImageField(upload_to='img', blank=True)

    def save(self, *args, **kwargs):
        if self.url == "#":
            print(
                "this is upload mode: this picture that user has upload needs to be upload to the subcribtions material space.")
            # print("self.content==None:", self.content == None, self.content == "", "xxx")
            # if self.content == "":
            #     print("this content is null:this picture is saved by URL from the Subcriptions.")
            # else:
            print(self.content)
            print(self.content.name)
            print(self.content.url)
            print(self.content.file)
            print(self.content.path)
            filepath = self.content.path
            with open(filepath, 'wb') as f:
                f.write(self.content.read())
            from .utils import upLoadImg
            url = "http://localhost:7000/miniProgram/getSubcribtionAccessToken"
            access_token = requests.get(url).text
            print("this is access_token by request the local server on the server:%s" % access_token)
            # virtualRequest.method = "GET"
            absoulutelyFilePath = os.path.abspath(filepath)
            print(absoulutelyFilePath)
            self.media_id, self.url = upLoadImg(absoulutelyFilePath, access_token, "image")
            if os.path.exists(absoulutelyFilePath):
                os.remove(absoulutelyFilePath)
            # self.content = None
        else:
            pass
        return super(Image, self).save(*args, **kwargs)

    def show(self):
        return format_html(
            '''<a href="%s"><img src="{}" width="200px" height="100px" onClick="copy(this,'src')"/></a>''',
            self.url, self.url
        )

    def getFromOriginHost(self):
        if self.content:
            if os.path.exists(self.content.path):
                print("该图片%s有缓存，不用下载到服务器:%s" % (self, self.content.path))
            else:
                self.downloadPictureToServer()
        else:
            self.downloadPictureToServer()
        return self.content.url

    def downloadPictureToServer(self):
        '''
        this is a function use to download the picture on the server disk as cache in order to resolve the Cross origin host.
        :return:Nothing
        '''
        print("该图片%s 在服务器上没有缓存，得重新下载：%s" % (self, self.url))
        CACHE_DIR_NAME = "ImgChageDIR"
        IMAGE_CHACHE_DIR = os.path.join(MEDIA_ROOT, CACHE_DIR_NAME)
        if not os.path.exists(IMAGE_CHACHE_DIR):
            os.makedirs(IMAGE_CHACHE_DIR)
        EXTENTION = ".png"
        if 'jpeg' in self.url or 'jpg' in self.url:
            EXTENTION = ".jpg"
        filename = "%s%s" % (self, EXTENTION)
        filePath = os.path.join(IMAGE_CHACHE_DIR, filename)
        print("this is the base name on the url:%s" % filePath)
        result = urllib.request.urlretrieve(self.url, filePath)
        print("下载好了：", result)
        self.content.save(
            os.path.join(CACHE_DIR_NAME, filename),  # 如果直接赋值 filename 则变成 img/filename.extention
            File(open(filePath, mode='rb'))
        )
        self.save()
    # def __str__(self):
    #     # return mark_safe('<img src="%s" width="50px" />' % (self.url))
    #     return


class ModelWithShowRate(MyModel):
    showTimes = models.IntegerField(verbose_name="被观看次数", default=0, )

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


class Film(ModelWithShowRate):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='电影标题', max_length=100)
    cover = models.URLField(verbose_name='电影封面',
                            default='https://mmbiz.qpic.cn/mmbiz_png/lBSHibv6GicCZ6TSPK91xVfqr0cGAiany3uOqL6lz3QvMMmGRdib5QaDxF6kN1JKIQRl4xVWH7yW2GIqn4J4ZdkE9A/0?wx_fmt=png',
                            blank=True)
    cover1 = models.ForeignKey(to=Image, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name

    def json(self, withEpisodes):
        json_object = {'film_id': self.id, 'name': self.name, 'cover': self.cover1.url}
        if withEpisodes:
            episodes = Video.objects.filter(belongTo=self).order_by('-episodeNum', '-last_changed_time')
            episodes_list = []
            # episodes_dic = {}
            for per_episode in episodes:
                episodes_list.append(per_episode.json())
                # episodes_dic.setdefault(per_episode.id, per_episode.json())
            json_object["episodes"] = episodes_list
            # json_object["latest_episode_id"] = episodes[0].id
        else:
            pass
        return json_object

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        print("this Film :%s has been updated now. force_insert:%s force_update:%s," % (
            self.name, force_insert, force_update), using, update_fields)
        return super(Film, self).save(force_update=force_update, force_insert=force_insert, using=using,
                                      update_fields=update_fields)

    showTimes = models.IntegerField(verbose_name="被观看次数", default=0, )


class Video(ModelWithShowRate):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='每一集的名字', max_length=50)
    episodeNum = models.IntegerField(verbose_name='集次', null=True)
    cover = models.ForeignKey(to=Image, on_delete=models.DO_NOTHING, blank=True, default=32)
    url = models.URLField(verbose_name='公众号文章链接', default="视频不见了的视频的链接", blank=True)
    belongTo = models.ForeignKey(verbose_name="所属电视剧", to=Film, on_delete=models.PROTECT, null=True)
    vid = models.CharField(verbose_name="vid", max_length=23, default=None, blank=True, null=True)

    def show(self):
        self.belongTo.show()
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
        print("this is getPureVideoUrl:", self, videoInfo)
        original_url = videoInfo['url_info'][0]['url']
        return original_url

    def isTXV(self):
        return "wxv_" not in self.vid

    def __str__(self):
        return self.name

    def json(self):
        # if not self.hasFirstAnalysed:
        #     self.analyse()
        if "wxv_" in self.vid:
            self.isTXV = False
        else:
            self.isTXV = True

        return {'vid': self.id, 'film_id': self.belongTo.id, 'name': self.name, 'cover': self.cover.url,
                'isTXV': self.isTXV, 'TXVid': self.vid, 'url': self.url,
                'video_url': "https://x.izbasarweb.xyz/miniProgram/videoUrlVid=%d" % self.id}

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        print("this Video :%s has been saved now. force_insert:%s force_update:%s," % (
            self.name, force_insert, force_update), using, update_fields)
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
        return "%f%s" % (self.size, self.unit.__str__())


class House(ModelWithShowRate):
    houseType = models.ForeignKey(to=HouseType, on_delete=models.CASCADE)
    houseLayout = models.ForeignKey(to=HouseLayout, on_delete=models.CASCADE, null=True)
    # size = models.FloatField(verbose_name="占地面积(m2)", default=103)
    size = models.ForeignKey(to=HouseSize, on_delete=models.CASCADE, verbose_name="占地面积", null=True)
    price = models.ForeignKey(to=HousePrice, on_delete=models.CASCADE, null=True)
    phoneNum = models.ForeignKey(to=PhoneNumber, on_delete=models.CASCADE, null=True)
    address = models.TextField()
    descriptions = models.TextField()
    images = models.ManyToManyField(to=Image)

    def json(self):
        images_list = []
        for per in self.images.all():
            images_list.append(per.url)
        return {'houseType': self.houseType.__str__(), 'houseLayout': self.houseLayout.__str__(),
                'address': "地址：%s" % self.address,
                'descriptions': self.descriptions,
                'phoneNum': self.phoneNum.json(), 'size': self.size.__str__(),
                'price': self.price.__str__(), 'images': images_list}


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
    sliders = models.ManyToManyField(to=Video)
    subcribtion = models.ForeignKey(to=subcribtions, on_delete=models.PROTECT, null=True)
    enableVIP_mode = models.BooleanField(verbose_name="是否启动VIP模式")
    VIPprice = models.FloatField(verbose_name="一个月会员价", null=True)
    trialTime = models.IntegerField(verbose_name="试看时间（秒）", default=5 * 60)

    def __str__(self):
        return self.app_name

    def json(self):
        return {
            "enableVIP_mode": self.enableVIP_mode,
            "VIPprice": self.VIPprice,
            "trialTime": self.trialTime,
        }
