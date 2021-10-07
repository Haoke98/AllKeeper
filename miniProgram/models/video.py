from django.db import models
from django.forms import ModelForm
from django.utils.html import format_html

from izBasar.models import ModelWithShowRate
from .film import Film
from .image import Image
from ..utils import getVideoInfo


class Video(ModelWithShowRate):
    id = models.AutoField(primary_key=True)
    episodeNum = models.IntegerField(verbose_name='集次', null=True, default=0)
    cover = models.ForeignKey(to=Image, on_delete=models.DO_NOTHING, blank=True, null=False, default=4)
    url = models.URLField(verbose_name='公众号文章链接', default="视频不见了的视频的链接", blank=True)
    film = models.ForeignKey(verbose_name="所属电视剧", to=Film, on_delete=models.PROTECT, null=True)
    vid = models.CharField(verbose_name="vid", max_length=23, default=None, blank=True, null=True)
    is_hot = models.BooleanField(verbose_name="是否被推", default=False, blank=True)

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = "所有" + verbose_name

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
        return format_html("{}{}", self.film, self.episode_name())

    def episode_name(self):
        if self.episodeNum == 0:
            return ""
        else:
            a = format_html("؛{}-{}", self.episodeNum, self.film.type.unit)
            return a

    def json(self, isForSlider):
        if "wxv_" in self.vid:
            self.isTXV = False
        else:
            self.isTXV = True
        if isForSlider:
            cover = self.cover.original_url
        else:
            cover = self.film.cover.original_url

        return {'vid': self.id, 'film_id': self.film.id, 'name': self.episode_name(),
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
        fields = ['episodeNum', 'url', 'film', 'vid']
