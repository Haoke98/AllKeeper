import os
from datetime import datetime

import requests
from django.db import models
# Create your models here.
from django.utils import timezone
from django.utils.html import format_html

from .utils import analyseArticleUrl, analyseArticleUrl2


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


class Article(MyModel):
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
    media_id = models.CharField(max_length=43, blank=True)
    url = models.URLField(blank=True)
    content = models.ImageField(upload_to='img', blank=True)

    def save(self, *args, **kwargs):
        print("self.content==None:", self.content == None, self.content == "", "xxx")
        if self.content == "":
            print("this content is null:this picture is saved by URL from the Subcriptions.")
        else:
            print("this is content is full:this picture is upload to the Subcribtions.")
            print(self.content)
            print(self.content.name)
            print(self.content.url)
            print(self.content.file)
            print(self.content.path)
            filepath = './%d' % (timezone.now().time().microsecond) + self.content.name
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
            if os.path.exists(filepath):
                os.remove(filepath)
            self.content = None
        return super(Image, self).save(*args, **kwargs)

    def show(self):
        return format_html(
            '''<a href="%s"><img src="{}" width="200px" height="100px" onClick="copy(this,'src')"/></a>''',
            self.url, self.url
        )
    # def __str__(self):
    #     # return mark_safe('<img src="%s" width="50px" />' % (self.url))
    #     return


class Film(MyModel):
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

    def show(self):
        self.showTimes += 1
        # self.save()


class Video(MyModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='每一集的名字', max_length=50)
    episodeNum = models.IntegerField(verbose_name='集次', null=True)
    cover = models.ForeignKey(to=Image, on_delete=models.DO_NOTHING, blank=True, default=32)
    url = models.URLField(verbose_name='公众号文章链接', default="视频不见了的视频的链接", blank=True)
    video_url = models.URLField(verbose_name='纯视频链接',
                                default="https://x.izbasarweb.xyz/miniProgram/UrlRedirector8")
    belongTo = models.ForeignKey(verbose_name="所属电视剧", to=Film, on_delete=models.PROTECT, null=True)
    showTimes = models.IntegerField(verbose_name="被观看次数", default=0, )
    isFromSubscription = models.BooleanField(verbose_name="来自公众号文章（需要解析）", default=True)
    hasFirstAnalysed = models.BooleanField(verbose_name="已经进行过首次解析", default=False)
    hasAnalysed = models.BooleanField(verbose_name="已经解析过", default=False)
    isTXV = models.BooleanField(verbose_name="是腾讯视频", default=False)
    TXVid = models.CharField(verbose_name="腾讯视频ID", max_length=11, default=None, blank=True)
    WXVid = models.CharField(verbose_name="公众号视频ID", max_length=23, default=None, blank=True, null=True)
    formatID = models.CharField(verbose_name="视频编码ID(决定视频流清晰度)", max_length=5, default="10002", blank=True, null=True)
    destinationID = models.CharField(verbose_name="视频临时连接中的不变头部", max_length=36, default=None, blank=True, null=True)

    analysedUrl = models.CharField(verbose_name="解析后的临时URL(有有效期)", max_length=400, default="#", blank=True, null=True)
    analysedUrl_ExpiredTime = models.DateTimeField(verbose_name="解析后URL的过期DDL", auto_now_add=True)

    def getAnalysedURL(self):
        if self.isTXV:
            return ""
        else:
            if not self.hasFirstAnalysed:
                self.analyse()
            if self.analysedUrl_ExpiredTime > timezone.now():
                print("this video:%s analysedURL has not been expired now." % self.name)
                return self.analysedUrl
            else:
                print("this video:%s analysedURL has been expired." % self.name)
                self.analysedUrl = analyseArticleUrl2(self.url, self.WXVid, self.formatID, self.destinationID)
                self.setExpiredTime()
                self.save()
                return self.analysedUrl

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

    def setExpiredTime(self):
        now = timezone.now()
        newHour = now.hour
        newDay = now.day
        newMonth = now.month
        newYear = now.year
        if newHour > 23:
            newDay += 1
            newHour -= 23
            if newMonth in [1, 3, 5, 7, 8, 10, 11]:
                if newDay > 31:
                    newMonth += 1
                    newDay -= 31
            else:
                if newDay > 30:
                    newMonth += 1
                    newDay -= 30
            if newMonth > 12:
                newYear += 1
                newMonth -= 12
        newDatetime = datetime(year=newYear, month=newMonth, day=newDay, hour=newHour,
                               minute=now.minute,
                               second=now.second, tzinfo=now.tzinfo)
        self.analysedUrl_ExpiredTime = newDatetime

    def analyse(self):
        print("正在对视频进行提前解析：%s" % self.name)
        self.isTXV, Vid, _id, formatID, tempURl = analyseArticleUrl(self.url)
        if self.isTXV:
            self.TXVid = Vid
        else:
            self.WXVid = Vid
            self.destinationID = _id
            self.formatID = formatID
            self.analysedUrl = tempURl
            self.setExpiredTime()
        self.hasAnalysed = True
        self.hasFirstAnalysed = True
        self.save()

    def show(self):
        self.showTimes += 1
        self.belongTo.show()
        self.save()

    def __str__(self):
        return self.name

    def json(self):
        if not self.hasFirstAnalysed:
            self.analyse()
        return {'vid': self.id, 'film_id': self.belongTo.id, 'name': self.name, 'cover': self.cover.url,
                'isTXV': self.isTXV, 'TXVid': self.TXVid, 'url': self.url,
                'video_url': self.video_url}

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        print("this Video :%s has been saved now. force_insert:%s force_update:%s," % (
            self.name, force_insert, force_update), using, update_fields)
        if self.isFromSubscription:
            if not self.hasFirstAnalysed:
                self.analyse()
            if not self.hasAnalysed:
                self.getAnalysedURL()
        else:
            pass
        self.belongTo.save(force_update=True)
        return super(Video, self).save(force_update=force_update, force_insert=force_insert, using=using,
                                       update_fields=update_fields)


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

    def __str__(self):
        return self.app_name

    def json(self):
        return {
            "enableVIP_mode": self.enableVIP_mode,
            "VIPprice": self.VIPprice,
        }
