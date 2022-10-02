from django.db import models

from izBasar.models import BaseModel
from .email import Email
from .group import Group
from .tel import Tel
from .type import Type
from .wechat import Wechat


class Account(BaseModel):
    group = models.ForeignKey(verbose_name="所属个体/组织", to=Group, on_delete=models.CASCADE, null=True, blank=False)
    platform = models.ForeignKey(verbose_name="所属平台", to=Type, on_delete=models.CASCADE, related_name="platform",
                                 null=True, limit_choices_to=models.Q(url__isnull=False))
    username = models.CharField(max_length=40, verbose_name="用户名")
    pwd = models.CharField(max_length=32, verbose_name="密码", null=True, blank=False)
    tels = models.ManyToManyField(verbose_name="所有绑定的手机号", to=Tel, related_name="tels", blank=True)
    emails = models.ManyToManyField(verbose_name="所有绑定的电子邮箱", to=Email, related_name="emails", blank=True)
    wechat = models.ForeignKey(verbose_name='绑定的微信', blank=True, null=True, on_delete=models.CASCADE, to=Wechat)
    info = models.TextField(verbose_name="说明", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="账号归属", null=True, blank=True)
    url = models.URLField(verbose_name="网站地址", null=True, blank=True)
    types = models.ManyToManyField(verbose_name="类型", to=Type, related_name='accountTypes', blank=True,
                                   limit_choices_to=models.Q(url__isnull=True))

    class Meta:
        verbose_name = "通用账号"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return "%s账号" % self.name
