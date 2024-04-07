import os.path
import uuid

import requests
from django.db import models
from simplepro.models import BaseModel

from proj.settings import MEDIA_ROOT
from utils import weiboHelper


# Create your models here.
class Weibo(BaseModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="昵称", null=True, blank=True)
    school = models.CharField(max_length=100, verbose_name="学校", null=True, blank=True)
    birthday = models.DateField(verbose_name="出生日期", null=True, blank=True)
    followersCount = models.IntegerField(verbose_name="粉刺数量", default=0)
    friendsCount = models.IntegerField(verbose_name="关注数量", default=0)
    statusesCount = models.IntegerField(verbose_name="内容数量", default=0)
    zodiac = models.CharField(verbose_name='星座', max_length=50, null=True, blank=True)
    registeredAt = models.DateTimeField(verbose_name="注册日期", null=True, blank=True)
    description = models.CharField(verbose_name="简介", null=True, blank=True, max_length=100)
    gender = models.CharField(max_length=1, verbose_name="性别", choices=(('m', '男'), ('f', '女')), null=True, blank=True)
    location = models.CharField(max_length=100, verbose_name="位置", null=True, blank=True)
    ipLocation = models.CharField(max_length=100, verbose_name="IP位置", null=True, blank=True)
    sunshineCredit = models.CharField(max_length=50, verbose_name="阳光信用", null=True, blank=True)
    userType = models.IntegerField(null=True, blank=True)
    mbrank = models.IntegerField(null=True, blank=True, verbose_name="VIP等级")
    mbtype = models.IntegerField(null=True, blank=True)
    isSVIP = models.BooleanField(verbose_name="是否为SVIP", default=False)
    pcNew = models.IntegerField(null=True, blank=True)
    labels = models.CharField(max_length=255, null=True, blank=True, verbose_name="标签")
    AVATAR_UPLOAD_TO = "weibo_avatar"
    avatar = models.ImageField(upload_to=AVATAR_UPLOAD_TO, verbose_name='头像', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = "微博账户"
        verbose_name_plural = "微博账户库"

    def __str__(self):
        if self.name:
            return f"{self.name}({self.id})"
        return f"微博账户({self.id})"

    def set_online_avatar(self, uri):
        avatarResp = requests.get(uri)
        contentType = avatarResp.headers['Content-Type']
        if 'jpeg' in contentType:
            ext = "jpeg"
        elif "gif" in contentType:
            ext = "gif"
        else:
            raise Exception(f"{contentType} is Unknown")
        avatar_fn = f"{uuid.uuid4().hex}.{ext}"
        avatar_fp = os.path.join(MEDIA_ROOT, os.path.join(self.AVATAR_UPLOAD_TO, avatar_fn))
        avatar_uri = f"/{self.AVATAR_UPLOAD_TO}/{avatar_fn}"
        print("保存头像：", avatar_fp)
        print("可访问URL：", avatar_uri)
        with open(avatar_fp, 'wb') as f:
            f.write(avatarResp.content)
        self.avatar = avatar_uri

    def collect(self):
        isOk, infoResp = weiboHelper.info(self.id)
        if isOk:
            detailResp = weiboHelper.detail(self.id)
            userInfo = infoResp['user']
            print("==========================" * 4)
            print(userInfo)
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^" * 4)
            self.name = userInfo['screen_name']
            self.set_online_avatar(userInfo['profile_image_url'])
            self.description = userInfo['description']
            self.location = userInfo['location']
            self.gender = userInfo['gender']
            self.followersCount = userInfo['followers_count']
            self.friendsCount = userInfo['friends_count']
            self.statusesCount = userInfo['statuses_count']
            if userInfo['svip'] == 1:
                self.isSVIP = True
            self.userType = userInfo['user_type']
            self.mbrank = userInfo['mbrank']
            self.mbtype = userInfo['mbtype']
            self.pcNew = userInfo['pc_new']
            self.registeredAt = detailResp['created_at']
            self.ipLocation = detailResp['ip_location']
            if "-" in detailResp['birthday']:
                self.birthday, self.zodiac = detailResp['birthday'].split(' ')
            else:
                self.zodiac = detailResp['birthday']
            self.sunshineCredit = detailResp['sunshine_credit']['level']
            if detailResp.keys().__contains__('education'):
                self.school = detailResp['education']['school']
            labels = []
            for label in detailResp['label_desc']:
                labels.append(label['name'])
            self.labels = '|'.join(labels)
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
