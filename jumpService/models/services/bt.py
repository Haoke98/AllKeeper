from django.db import models
from simplepro.components.fields import PasswordInputField
from simplepro.models import BaseModel

from ..devices import ServerNew


class BT(BaseModel):
    port = models.PositiveIntegerField(verbose_name="端口", default=8888, blank=False)
    server = models.OneToOneField(verbose_name="宿机", to=ServerNew, on_delete=models.CASCADE, null=True, blank=False)
    username = models.CharField(max_length=32, verbose_name="用户", null=True, blank=False, help_text="请输入用户名")
    pwd = PasswordInputField(max_length=32, verbose_name="密码", null=True, blank=False)
    basicAuthUsername = models.CharField(max_length=32, verbose_name="BasicAuth用户", null=True, blank=True)
    basicAuthPwd = models.CharField(max_length=32, verbose_name="BasicAuth密码", null=True, blank=True)
    path = models.CharField(max_length=50, verbose_name="面板路径", null=True, blank=True)
    domain = models.URLField(verbose_name="绑定的域名", null=True, blank=True)

    class Meta:
        verbose_name = "宝塔"
        verbose_name_plural = f"所有{verbose_name}"
