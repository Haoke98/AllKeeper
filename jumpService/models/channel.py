# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/15
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.components import fields
from simplepro.models import BaseModel

from .devices import NetDevice


class Channel(BaseModel):
    left = fields.ForeignKey(to=NetDevice, on_delete=models.CASCADE, related_name='channel_left')
    right = fields.ForeignKey(to=NetDevice, on_delete=models.CASCADE, related_name='channel_right')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['left', 'right'], name='unique_channel_pair')
        ]
        verbose_name = "通道"
        verbose_name_plural = "通道"

    def __str__(self):
        return f"{self.left} <<==>> {self.right}"


class PortMap(BaseModel):
    left = fields.ForeignKey(to=NetDevice, on_delete=models.CASCADE, related_name='left_ports')
    leftPort = fields.IntegerField(null=True, blank=True)
    right = fields.ForeignKey(to=NetDevice, on_delete=models.CASCADE, related_name='right_ports')
    rightPort = fields.IntegerField(null=True, blank=True)

    # TODO: 通过两段的设备确认走的是那个通道, 尤其可以通过下游的端所在的所有网段中去搜

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['left', 'right'], name='unique_p2p'),
            models.UniqueConstraint(fields=['left', 'leftPort'], name='unique_left_port'),
            models.UniqueConstraint(fields=['right', 'rightPort'], name='unique_right_port'),
        ]
        verbose_name = "端口映射"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.left}:{self.leftPort} ===> {self.right}:{self.rightPort}"
