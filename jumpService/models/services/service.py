# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/15
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.components.fields import PasswordInputField, CharField
from simplepro.models import BaseModel

from ..devices import ServerNew


class BaseAccountModel(BaseModel):
    remark = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True, db_index=True)

    class Meta:
        abstract = True


class Service(BaseAccountModel):
    server = models.ForeignKey(to=ServerNew, on_delete=models.CASCADE, verbose_name="服务器", null=True,
                               blank=False, db_index=True)
    port = models.PositiveIntegerField(verbose_name="端口", default=8888, blank=False, db_index=True)

    class Meta:
        abstract = False
        verbose_name = "服务"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['server', 'port'], name="service_server_port_unique")
        ]

    def __str__(self):
        return f"服务({self.server.ip}:{self.port}）"


class ServiceUser(BaseModel):
    owner = models.CharField(verbose_name="使用者", max_length=50, null=True, blank=True)
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, verbose_name="服务", null=True,
                                blank=False)
    username = CharField(max_length=32, null=True, blank=False, verbose_name="用户名")
    password = PasswordInputField(max_length=32, null=True, blank=False, verbose_name="密码", size="medium",
                                  style="width:600px;", pattern="123456789,.asdfgzxcvbnm")
    hasRootPriority = models.BooleanField(default=False, verbose_name="拥有root权限", blank=True)

    class Meta:
        abstract = False
        verbose_name = "服务用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"用户（{self.service.server.ip},{self.owner}）"


class AbstractBaseServiceModel(BaseAccountModel):
    server = models.ForeignKey(to=ServerNew, on_delete=models.CASCADE, verbose_name="服务器", null=True,
                               blank=False, db_index=True)
    port = models.PositiveIntegerField(verbose_name="端口", default=8888, blank=False, db_index=True)

    class Meta:
        abstract = True
        verbose_name = "服务"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['server', 'port'], name="service_server_port_unique")
        ]

    def __str__(self):
        return f"服务({self.server.ip}:{self.port}）"


class AbstractBaseServiceUserModel(BaseModel):
    owner = models.CharField(verbose_name="使用者", max_length=50, null=True, blank=True)
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, verbose_name="服务", null=True,
                                blank=False)
    username = CharField(max_length=32, null=True, blank=False, verbose_name="用户名")
    password = PasswordInputField(max_length=32, null=True, blank=False, verbose_name="密码", size="medium",
                                  style="width:600px;", pattern="123456789,.asdfgzxcvbnm")
    hasRootPriority = models.BooleanField(default=False, verbose_name="拥有root权限", blank=True)

    class Meta:
        abstract = True
        verbose_name = "服务用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"用户（{self.service.server.ip},{self.owner}）"
