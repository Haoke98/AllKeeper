# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/27
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.components import fields
from simplepro.models import BaseModel

from .device import Device


class Net(BaseModel):
    content = fields.CharField(max_length=15)
    remark = fields.CharField(verbose_name="备注", max_length=100)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "网段"
        verbose_name_plural = verbose_name


class NetDevice(Device):
    mac = models.CharField(max_length=17, verbose_name="MAC地址", blank=True, null=True)

    class Meta:
        verbose_name = "网络设备"
        verbose_name_plural = verbose_name


class IPAddress(BaseModel):
    net = models.ForeignKey(to=Net, verbose_name="所属网段", on_delete=models.CASCADE, null=True, blank=True)
    ip = fields.CharField(verbose_name="IP地址", null=True, blank=False, slot_text="IPV4/IPV6", slot="prepend",
                          max_length=15)
    device = models.ForeignKey(verbose_name="网络设备", to=NetDevice, on_delete=models.CASCADE, null=True, blank=False,
                               help_text="是指占用当前地址的网络设备")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ip', 'net'], name="net_ip_unique")
        ]
