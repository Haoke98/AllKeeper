from django.db import models

from .tel import Tel
from .group import Group
from .password import Password
from izBasar.models import BaseModel


class Wechat(BaseModel):
    wx_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nickName = models.CharField(max_length=20, null=True, blank=True)
    password = models.ForeignKey(to=Password, on_delete=models.CASCADE, verbose_name="密码", null=True, blank=True)
    tel = models.OneToOneField(verbose_name="绑定的手机号", to=Tel, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(verbose_name="所属账号组", to=Group, on_delete=models.CASCADE, null=True, blank=True)
    remark = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "微信"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        if self.remark is None:
            return "微信(%s)" % self.ID
        else:
            return "微信(%s,%s)" % (self.ID, self.remark)
