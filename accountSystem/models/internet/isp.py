# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/28
@Software: PyCharm
@disc:
======================================="""
from django.db import models

from izBasar.models import BaseModel


class Isp(BaseModel):
    name = models.CharField(max_length=50)
