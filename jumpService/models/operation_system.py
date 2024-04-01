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
from simplepro.lib import pkHelper
from simplepro.models import BaseModel

from .devices import ServerNew


class OperationSystemImage(BaseModel):
    id = fields.CharField(max_length=48, primary_key=True, editable=False, default=pkHelper.uuid_generator)
    name = fields.CharField(max_length=50, verbose_name="名称")
    version = fields.CharField(max_length=50, verbose_name="版本")

    isLTS = models.BooleanField(default=False, verbose_name="LTS")
    arch = fields.CharField(max_length=50, verbose_name="ARCH", null=True, help_text="什么架构?比如: 32bit or 64bit",
                            blank=True)
    iso = models.FileField(verbose_name="镜像", upload_to='system_images', null=True, blank=True)

    class Meta:
        verbose_name = "操作系统镜像"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['name', 'version', 'arch'], name="operation_system_name_version_unique")
        ]

    def __str__(self):
        return f"{self.name}{self.version}"


class OperationSystem(BaseModel):
    image = fields.ForeignKey(to=OperationSystemImage, on_delete=models.CASCADE, null=True, blank=False,
                              verbose_name="系统镜像")
    server = fields.ForeignKey(to=ServerNew, on_delete=models.CASCADE, null=True, blank=False, verbose_name="服务器",
                               related_name="systems")
    rootUsername = models.CharField(max_length=32, verbose_name="root用户名", blank=False, default="root")
    rootPassword = fields.PasswordInputField(max_length=32, verbose_name="root密码", blank=False, null=True)

    class Meta:
        verbose_name = "操作系统"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.image}-{self.server}"
