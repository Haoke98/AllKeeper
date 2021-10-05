from django.db import models

from .accountType import AccountType
from .base import BaseModel
from .models import PPassword, TTel, EEmail, Group


class Account(BaseModel):
    name = models.CharField(max_length=50, verbose_name="账号归属", default="未知账号")
    username = models.CharField(max_length=40, verbose_name="用户名")
    password = models.ForeignKey(to=PPassword, on_delete=models.CASCADE, verbose_name="密码", null=True)
    tel = models.ForeignKey(verbose_name="绑定的手机号", to=TTel, on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField(verbose_name="网站地址", null=True, blank=True)
    email = models.ForeignKey(verbose_name="关联邮箱", to=EEmail, on_delete=models.CASCADE, null=True, blank=True)
    info = models.TextField(verbose_name="说明", null=True, blank=True)
    group = models.ForeignKey(verbose_name="所属账号组", to=Group, on_delete=models.CASCADE, null=True, blank=True)
    icon = models.ImageField(verbose_name="图标", null=True, blank=True)
    type = models.ForeignKey(verbose_name="类型", to=AccountType, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "account"
        verbose_name = "账号"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return "%s账号" % self.name
