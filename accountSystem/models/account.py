from django.db import models

from izBasar.models import BaseModel
from .email import Email
from .group import Group
from .password import Password
from .tel import Tel
from .type import Type


class Account(BaseModel):
    name = models.CharField(max_length=50, verbose_name="账号归属", default="未知账号")
    username = models.CharField(max_length=40, verbose_name="用户名")
    password = models.ForeignKey(to=Password, on_delete=models.CASCADE, verbose_name="密码", null=True)
    types = models.ManyToManyField(verbose_name="类型", to=Type, related_name='accountTypes')
    url = models.URLField(verbose_name="网站地址", null=True, blank=True)
    tels = models.ManyToManyField(verbose_name="所有绑定的手机号", to=Tel, related_name="tels", blank=True)
    emails = models.ManyToManyField(verbose_name="所有绑定的电子邮箱", to=Email, related_name="emails", blank=True)
    group = models.ForeignKey(verbose_name="所属账号组", to=Group, on_delete=models.CASCADE, null=True, blank=True)
    info = models.TextField(verbose_name="说明", null=True, blank=True)
    icon = models.ImageField(verbose_name="图标", null=True, blank=True)

    class Meta:
        verbose_name = "账号"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return "%s账号" % self.name
