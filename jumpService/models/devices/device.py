# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/28
@Software: PyCharm
@disc:
======================================="""
from simplepro.components import fields
from simplepro.lib import pkHelper
from simplepro.models import BaseModel
from django.db import models


from ..brand import Brand


class Device(BaseModel):
    id = fields.CharField(max_length=48, primary_key=True, default=pkHelper.uuid_generator)
    brand = fields.ForeignKey(Brand, on_delete=models.CASCADE, related_name='devices', null=True, blank=True)
    remark = fields.CharField(verbose_name="备注", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "设备"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.remark:
            return f"设备({self.id},{self.remark})"
        else:
            return f"设备({self.id})"


class DeviceStatus(BaseModel):
    id = fields.CharField(max_length=48, primary_key=True, default=pkHelper.uuid_generator)
    content = models.CharField(max_length=100, verbose_name="状态内容")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True, verbose_name="所属设备")
    ip = fields.CharField(verbose_name="IP地址", max_length=50, null=True, blank=True)
    errno = fields.CharField(verbose_name="错误代码", max_length=50, null=True, blank=True)
    errstr = models.TextField(verbose_name="详细内容", null=True, blank=True)

    class Meta:
        verbose_name = "设备状态"
        verbose_name_plural = verbose_name
