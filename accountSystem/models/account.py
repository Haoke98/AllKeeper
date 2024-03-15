from django.db import models
from simplepro.components import fields

from .baseAccount import BaseAccount
from .email import Email
from .tel import Tel
from .platform import Platform
from .wechat import Wechat


class Account(BaseAccount):
    platform = fields.ForeignKey(verbose_name="所属平台", to=Platform, on_delete=models.CASCADE, related_name="platform",
                                 null=True, limit_choices_to=models.Q(url__isnull=False))
    tels = fields.ManyToManyField(verbose_name="所有绑定的手机号", to=Tel, related_name="tels", blank=True)
    emails = fields.ManyToManyField(verbose_name="所有绑定的电子邮箱", to=Email, related_name="emails", blank=True)
    wechat = fields.ForeignKey(verbose_name='绑定的微信', blank=True, null=True, on_delete=models.CASCADE, to=Wechat)
    name = fields.CharField(max_length=50, verbose_name="账号归属", null=True, blank=True)
    url = models.URLField(verbose_name="网站地址", null=True, blank=True)
    types = fields.ManyToManyField(verbose_name="类型", to=Platform, related_name='accountTypes', blank=True,
                                   limit_choices_to=models.Q(url__isnull=True))

    class Meta:
        verbose_name = "通用账号"
        verbose_name_plural = "所有" + verbose_name
        ordering = ['-updatedAt']

    def __str__(self):
        return "%s账号" % self.name
