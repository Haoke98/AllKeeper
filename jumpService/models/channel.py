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
