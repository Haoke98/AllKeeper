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


class Device(BaseModel):
    status = fields.CharField(verbose_name='状态', max_length=50, null=True, blank=True)
    remark = fields.CharField(verbose_name="备注", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "设备"
        verbose_name_plural = verbose_name
