import os
import urllib

from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.html import format_html

from izBasar.settings import MEDIA_ROOT
from .base import MyModel
from miniProgram.utils import upLoadImg
from miniProgram.views import subscriptionAccountService


class Image(MyModel):
    id = models.AutoField(primary_key=True)
    media_id = models.CharField(max_length=43, blank=True, default="#")
    # url_default_choices = (("#", "#"),)
    # url = models.CharField(max_length=500, blank=True, default="#",choices=url_default_choices)
    url = models.CharField(max_length=500, blank=True, default="#")
    content = models.ImageField(upload_to='img', blank=True)

    def save(self, *args, **kwargs):
        if self.url == "#":
            fileExtension = os.path.splitext(self.content.path)[-1]
            tempFileName = "%s%s" % (str(datetime.now().microsecond), fileExtension)
            tempFilePath = os.path.join(MEDIA_ROOT, tempFileName)
            with open(tempFilePath, 'wb') as f:
                f.write(self.content.read())
            try:
                accessToken = subscriptionAccountService.getAccessToken()
                print("accesstoken", accessToken)
                absolutelyFilePath = os.path.abspath(tempFilePath)
                self.media_id, self.url = upLoadImg(absolutelyFilePath, accessToken, "image")
                print(self.media_id, self.url)
                if os.path.exists(absolutelyFilePath):
                    os.remove(absolutelyFilePath)
            except BaseException as e:
                print("发生了异常", e)
        else:
            pass
        return super(Image, self).save(*args, **kwargs)

    def show(self):
        return format_html(
            '''<img src="{}" width="200px" height="100px"  title="{}" onClick="show_big_img(this)"/>''',
            self.url, "%s\n%s" %
                      (self.__str__(), self.url)

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
        print("this is the base.py name on the url:%s" % filePath)
        result = urllib.request.urlretrieve(self.url, filePath)
        print("下载好了：", result)
        self.content.save(
            os.path.join(CACHE_DIR_NAME, filename),  # 如果直接赋值 filename 则变成 img/filename.extention
            # File(open(filePath, mode='rb'))
        )
        self.save()
    # def __str__(self):
    #     # return mark_safe('<img src="%s" width="50px" />' % (self.url))
    #     return
