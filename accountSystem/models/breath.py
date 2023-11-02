# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/5/15
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.models import BaseModel


class BreathInfo(BaseModel):
    accessAt = models.DateTimeField(verbose_name="获取时间")
    latitude = models.FloatField(verbose_name="经度")
    longitude = models.FloatField(verbose_name="纬度")
    mac = models.CharField(max_length=50, verbose_name="设备的MAC地址")
    ip = models.CharField(max_length=50, verbose_name="设备的动态IP")
