# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/15
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.components import fields
from simplepro.lib import pkHelper
from simplepro.models import BaseModel

from ..devices import ServerNew
from ..operation_system import OperationSystem


class BaseAccountModel(BaseModel):
    id = fields.CharField(max_length=48, primary_key=True, editable=False, default=pkHelper.uuid_generator)
    remark = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True, db_index=True)

    class Meta:
        abstract = True


class ServiceType(BaseAccountModel):
    name = fields.CharField(max_length=50, verbose_name="名称")
    port = fields.IntegerField(verbose_name="默认端口", null=True, blank=True)
    dashboardPort = fields.IntegerField(verbose_name="默认Dashboard端口", null=True, blank=True)
    defaultSuperUsername = fields.CharField(max_length=50, verbose_name="默认超级用户名", null=True, blank=True)
    defaultSuperUserPwd = fields.CharField(max_length=50, verbose_name="默认超级用户密码", null=True, blank=True)
    doc = fields.CharField(max_length=500, verbose_name="文档地址", null=True, blank=True)
    official = fields.CharField(max_length=500, verbose_name="官网地址", null=True, blank=True)
    code = fields.CharField(max_length=500, verbose_name="源代码仓库地址",
                            placeholder="github/gitee/gitcode....等等开源代码仓库地址即可",
                            null=True, blank=True)

    class Meta:
        verbose_name = "服务类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class Service(BaseAccountModel):
    _type = fields.ForeignKey(to=ServiceType, on_delete=models.CASCADE, verbose_name="服务类型", null=True, blank=False)
    system = fields.ForeignKey(to=OperationSystem, on_delete=models.CASCADE, verbose_name="操作系统", null=True,
                               blank=False)
    port = models.PositiveIntegerField(verbose_name="端口", null=True, blank=True, db_index=True)
    sslOn = models.BooleanField(verbose_name="SSL", default=False)
    dashboardPort = models.PositiveIntegerField(verbose_name="Dashboard/Console端口", null=True, blank=True,
                                                db_index=True)
    dashboardPath = models.TextField(verbose_name="路径", null=True, blank=True)

    # TODO: 确定单用户服务和多用户服务之间的关系的处理, 要分开还是统一处理?

    class Meta:
        abstract = False
        verbose_name = "服务"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['system', 'port'], name="service_server_port_unique")
        ]

    def __str__(self):
        return f"{self._type.name}服务({self.system}:{self.port}）"


class ServiceUser(BaseModel):
    owner = models.CharField(verbose_name="使用者", max_length=50, null=True, blank=True)
    service = fields.ForeignKey(to=Service, on_delete=models.CASCADE, verbose_name="服务", null=True,
                                blank=False)
    username = fields.CharField(max_length=32, null=True, blank=False, verbose_name="用户名")
    password = fields.PasswordInputField(max_length=32, null=True, blank=False, verbose_name="密码", size="medium",
                                         style="width:600px;", pattern="123456789,.asdfgzxcvbnm")
    hasRootPriority = models.BooleanField(default=False, verbose_name="拥有root权限", blank=True)

    class Meta:
        abstract = False
        verbose_name = "服务用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"用户（{self.service},{self.owner}）"


class AbstractBaseServiceModel(BaseAccountModel):
    server = models.ForeignKey(to=ServerNew, on_delete=models.CASCADE, verbose_name="服务器", null=True,
                               blank=False, db_index=True, related_name="services")
    port = models.PositiveIntegerField(verbose_name="端口", default=8888, blank=False, db_index=True)
    path = models.TextField(verbose_name="路径", null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = "服务"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['server', 'port'], name="service_server_port_unique")
        ]

    def __str__(self):
        return f"服务({self.server}:{self.port}）"


class AbstractBaseServiceUserModel(BaseModel):
    id = models.CharField(max_length=48, primary_key=True, default=pkHelper.uuid_generator)
    owner = models.CharField(verbose_name="使用者", max_length=50, null=True, blank=True)
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, verbose_name="服务", null=True,
                                blank=False)
    username = fields.CharField(max_length=32, null=True, blank=False, verbose_name="用户名")
    password = fields.PasswordInputField(max_length=32, null=True, blank=False, verbose_name="密码", size="medium",
                                         style="width:600px;", pattern="123456789,.asdfgzxcvbnm")
    hasRootPriority = models.BooleanField(default=False, verbose_name="拥有root权限", blank=True)

    class Meta:
        abstract = True
        verbose_name = "服务用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"用户（{self.service},{self.owner}）"
