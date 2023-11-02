# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/6/27
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.models import BaseModel


class MarketSubject(BaseModel):
    name = models.CharField(max_length=100, verbose_name="名称")
    ucc = models.CharField(max_length=18, verbose_name="统一信用代码", null=True, blank=True)

    def __str__(self):
        if self.ucc:
            return f"{self.name}({self.ucc})"
        return self.name

    class Meta:
        verbose_name = "市场主体"
        verbose_name_plural = verbose_name
