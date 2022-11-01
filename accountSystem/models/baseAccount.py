# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/10/17
@Software: PyCharm
@disc:
======================================="""
from django.db import models

from izBasar.models import BaseModel
from .group import Group


class BaseAccount(BaseModel):
    group = models.ForeignKey(verbose_name="所属", to=Group, on_delete=models.CASCADE, null=True, blank=False)
    username = models.CharField(max_length=40, verbose_name="用户名", null=True)
    pwd = models.CharField(max_length=32, verbose_name="密码", null=True, blank=False)

    class Meta:
        abstract = True
