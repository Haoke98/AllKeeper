from django.db import models
from izBasar.models import BaseModel
from .server import Server
from .password import Password


class BT(BaseModel):
    port = models.PositiveIntegerField(verbose_name="端口", default=8888, blank=False)
    server = models.OneToOneField(verbose_name="宿机", to=Server, on_delete=models.CASCADE, null=True, blank=False)
    username = models.CharField(max_length=32, verbose_name="用户名", null=True, blank=False)
    password = models.ForeignKey(to=Password, on_delete=models.CASCADE, verbose_name="密码", null=True, blank=False)
    basicAuthUsername = models.CharField(max_length=32, verbose_name="BasicAuth用户名", null=True, blank=True)
    basicAuthPassword = models.ForeignKey(to=Password, related_name="basicAuthPassword", on_delete=models.CASCADE,
                                          verbose_name="BasicAuth密码", null=True, blank=True)
    path = models.CharField(max_length=50, verbose_name="面板路径", null=True, blank=True)
    domain = models.URLField(verbose_name="绑定的域名", null=True, blank=True)

    class Meta:
        verbose_name = "宝塔"
        verbose_name_plural = f"所有{verbose_name}"
