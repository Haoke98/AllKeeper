import os
import urllib

from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.html import format_html

from izBasar.models import BaseModel
from izBasar.settings import IMAGE_ROOT
from miniProgram.utils import upLoadImg
from miniProgram.views.views import subscriptionAccountService


class Image(BaseModel):
    id = models.AutoField(primary_key=True)
    mediaId = models.CharField(max_length=43, blank=True, default="#")
    fileName = models.CharField(verbose_name="文件名", max_length=600, blank=True, default="#")
    originalUrl = models.CharField(verbose_name="原始链接（公众号）", max_length=500, blank=True, default="#")
    content = models.ImageField(upload_to='img', blank=True)

    class Meta:
        verbose_name = "图片"
        verbose_name_plural = "所有" + verbose_name

    def save(self, *args, **kwargs):
        if self.original_url == "#":
            fileExtension = os.path.splitext(self.content.path)[-1]
            self.fileName = "%s%s" % (str(datetime.now().microsecond), fileExtension)
            tempFilePath = os.path.join(IMAGE_ROOT, self.fileName)
            with open(tempFilePath, 'wb') as f:
                f.write(self.content.read())
            try:
                accessToken = subscriptionAccountService.getAccessToken()
                print("accesstoken", accessToken)
                absolutelyFilePath = os.path.abspath(tempFilePath)
                self.mediaId, self.original_url = upLoadImg(absolutelyFilePath, accessToken, "image")
                print(self.mediaId, self.original_url)
            except BaseException as e:
                print("发生了异常", e)
        else:
            pass
        return super(Image, self).save(*args, **kwargs)


    def show(self):
        return format_html(
            '''<img src="{}" width="200px" height="100px"  title="{}" onClick="show_big_img(this)"/>''',
            self.original_url, "%s\n%s" %
                               (self.__str__(), self.original_url)

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
        print("该图片%s 在服务器上没有缓存，得重新下载：%s" % (self, self.original_url))
        CACHE_DIR_NAME = "ImgChageDIR"
        IMAGE_CHACHE_DIR = os.path.join(MEDIA_ROOT, CACHE_DIR_NAME)
        if not os.path.exists(IMAGE_CHACHE_DIR):
            os.makedirs(IMAGE_CHACHE_DIR)
        EXTENTION = ".png"
        if 'jpeg' in self.original_url or 'jpg' in self.original_url:
            EXTENTION = ".jpg"
        filename = "%s%s" % (self, EXTENTION)
        filePath = os.path.join(IMAGE_CHACHE_DIR, filename)
        print("this is the base.py name on the url:%s" % filePath)
        result = urllib.request.urlretrieve(self.original_url, filePath)
        print("下载好了：", result)
        self.content.save(
            os.path.join(CACHE_DIR_NAME, filename),  # 如果直接赋值 filename 则变成 img/filename.extention
            # File(open(filePath, mode='rb'))
        )
        self.save()
    # def __str__(self):
    #     # return mark_safe('<img src="%s" width="50px" />' % (self.url))
    #     return
