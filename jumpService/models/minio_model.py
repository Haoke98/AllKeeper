# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/28
@Software: PyCharm
@disc:
======================================="""
from simplepro.components import fields

from .service import Service


class MinIO(Service):
    console_port = fields.IntegerField(verbose_name="Console端口")

    class Meta:
        verbose_name = "MinIO"
        verbose_name_plural = verbose_name
