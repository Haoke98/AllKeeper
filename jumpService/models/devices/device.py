# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/28
@Software: PyCharm
@disc:
======================================="""
from simplepro.components import fields
from simplepro.models import BaseModel

from lib import pkHelper


class Device(BaseModel):
    id = fields.CharField(max_length=48, primary_key=True, default=pkHelper.uuid_generator())
    status = fields.CharField(verbose_name='状态', max_length=50, null=True, blank=True)
    remark = fields.CharField(verbose_name="备注", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "设备"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.remark:
            return f"设备({self.id},{self.remark})"
        else:
            return f"设备({self.id})"
