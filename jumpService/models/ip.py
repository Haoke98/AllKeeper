# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/12/8
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.components import fields
from simplepro.models import BaseModel
from .devices import NetDevice
from .net import Net


class IPAddress(BaseModel):
    net = models.ForeignKey(to=Net, verbose_name="所属网段", on_delete=models.CASCADE, null=True, blank=True)
    ip = fields.CharField(verbose_name="IP地址", null=True, blank=False, slot_text="IPV4", slot="prepend",
                          max_length=15)
    device = models.ForeignKey(verbose_name="网络设备", to=NetDevice, on_delete=models.CASCADE, null=True, blank=False,
                               help_text="是指占用当前地址的网络设备", related_name="ips")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ip', 'net'], name="net_ip_unique")
        ]
        verbose_name = "IPAddress"
        verbose_name_plural = verbose_name
