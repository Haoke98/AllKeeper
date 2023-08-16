# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/8/16
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.components import fields

from izBasar.models import BaseModel


class Album(BaseModel):
    name = models.CharField(max_length=50, verbose_name="标题", primary_key=True)
    total = models.PositiveIntegerField(default=0, verbose_name="媒体数量")

    class Meta:
        verbose_name = "iCloud相册"


class IMedia(BaseModel):
    id = models.CharField(max_length=50, primary_key=True)
    filename = models.CharField(max_length=100, verbose_name="文件名")
    ext = models.CharField(max_length=10, verbose_name="扩展名")
    size = models.BigIntegerField(verbose_name="大小")
    dimensionX = models.IntegerField(verbose_name="DX")
    dimensionY = models.IntegerField(verbose_name="DY")
    asset_date = models.DateTimeField(verbose_name="生成时间")
    added_date = models.DateTimeField(verbose_name="加入icloud的时间")
    versions = models.TextField()
    video = fields.VideoField(max_length=600, verbose_name='播放', null=True, blank=True, help_text='视频播放组件')
    img = fields.ImageField(drag=False, accept=".png", verbose_name='预览', max_length=600, null=True, blank=True)

    class Meta:
        verbose_name = "iCloud媒体"
