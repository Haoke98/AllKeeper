# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/8/16
@Software: PyCharm
@disc:
======================================="""
from django.db import models

from izBasar.models import BaseModel


class IMedia(BaseModel):
    id = models.CharField(max_length=50, primary_key=True)
    filename = models.CharField(max_length=100, verbose_name="文件名")
    ext = models.CharField(max_length=10, verbose_name="扩展名")
    size = models.IntegerField(verbose_name="大小")
    dimensionX = models.IntegerField(verbose_name="DX")
    dimensionY = models.IntegerField(verbose_name="DY")
    asset_date = models.DateTimeField(verbose_name="生成时间")
    added_date = models.DateTimeField(verbose_name="加入icloud的时间")
    versions = models.TextField()

    class Meta:
        verbose_name = "icloud媒体"
