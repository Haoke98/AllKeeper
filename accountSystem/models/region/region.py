# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/28
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.models import BaseModel


class Region(BaseModel):
    nameEn = models.CharField(max_length=50, verbose_name="名称（英文）", unique=True, default="")
    nameCn = models.CharField(max_length=50, verbose_name="名称（中文）", unique=True, default="")

    class Meta:
        abstract = True
        ordering = ['-updatedAt']
