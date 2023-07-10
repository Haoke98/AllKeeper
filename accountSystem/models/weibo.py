import datetime

from django.db import models

from izBasar.models import BaseModel
from lib import zodiacHelper


# Create your models here.
class Weibo(BaseModel):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="昵称", null=True, blank=True)
    school = models.CharField(max_length=100, verbose_name="学校",null=True,blank=True)
    birthday = models.DateField(verbose_name="出生日期", null=True, blank=True)
    followersCount = models.IntegerField(verbose_name="粉刺数量",default=0)
    friendsCount = models.IntegerField(verbose_name="关注数量",default=0)
    statusesCount = models.IntegerField(verbose_name="内容数量",default=0)
    zodiac = models.CharField(verbose_name='星座', max_length=50, null=True, blank=True)
    registeredAt = models.DateTimeField(verbose_name="注册日期", null=True, blank=True)
    description = models.CharField(verbose_name="简介", null=True, blank=True, max_length=100)
    gender = models.CharField(max_length=1, verbose_name="性别", choices=(('m','男'),('f','女')), null=True,blank=True)
    location = models.CharField(max_length=100, verbose_name="位置", null=True, blank=True)
    ipLocation = models.CharField(max_length=100, verbose_name="IP位置", null=True, blank=True)
    sunshineCredit = models.CharField(max_length=50, verbose_name="阳光信用",  null=True, blank=True)
    isSVIP = models.BooleanField(verbose_name="是否为SVIP",default=False)
    userType = models.IntegerField(null=True,blank=True)
    avatar = models.CharField(max_length=255,null=True,blank=True,verbose_name="头像")


    class Meta:
        verbose_name = "微博账户"
        verbose_name_plural = "微博账户库"

    def __str__(self):
        if self.name:
            return f"{self.name}({self.id})"
        return f"微博账户({self.id})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
