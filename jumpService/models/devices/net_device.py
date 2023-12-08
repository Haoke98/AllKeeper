# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/12/8
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from .device import Device


class NetDevice(Device):
    mac = models.CharField(max_length=17, verbose_name="MAC地址", blank=True, null=True)

    class Meta:
        verbose_name = "网络设备"
        verbose_name_plural = verbose_name
