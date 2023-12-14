# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/12/11
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.components import fields
from simplepro.models import BaseModel

from .devices import ServerNew


class OperationSystemImage(BaseModel):
    name = fields.CharField(max_length=50, verbose_name="名称")
    version = fields.CharField(max_length=50, verbose_name="版本")

    class Meta:
        verbose_name = "操作系统镜像"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['name', 'version'], name="operation_system_name_version_unique")
        ]

    def __str__(self):
        return f"{self.name}{self.version}"


class OperationSystem(BaseModel):
    image = fields.ForeignKey(to=OperationSystemImage, on_delete=models.CASCADE, null=True, blank=False,
                              verbose_name="系统镜像")
    server = fields.ForeignKey(to=ServerNew, on_delete=models.CASCADE, null=True, blank=False, verbose_name="服务器")
    rootUsername = models.CharField(max_length=32, verbose_name="root用户名", blank=False, default="root")
    rootPassword = fields.PasswordInputField(max_length=32, verbose_name="root密码", blank=False, null=True)

    class Meta:
        verbose_name = "操作系统"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.image}-{self.server}"
