# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/28
@Software: PyCharm
@disc:
======================================="""
from django.db import models

from .region import Region


class Country(Region):
    code = models.CharField(max_length=4, verbose_name="英文编号", unique=True)
