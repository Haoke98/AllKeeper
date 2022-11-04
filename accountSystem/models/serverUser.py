from django.db import models

from izBasar.models import BaseModel
from .human import Human
from .server import Server


class ServerUser(BaseModel):
    owner = models.ForeignKey(verbose_name="所属个体/组织", to=Human, on_delete=models.CASCADE, null=True, blank=True)
    server = models.ForeignKey(to=Server, on_delete=models.CASCADE, verbose_name="服务器", null=True,
                               blank=False)
    username = models.CharField(max_length=32, null=True, blank=False, verbose_name="用户名")
    pwd = models.CharField(max_length=32, verbose_name="密码", null=True, blank=False)
    hasRootPriority = models.BooleanField(default=False, verbose_name="拥有root权限", blank=True)

    class Meta:
        verbose_name = "服务器用户"
        verbose_name_plural = f"所有{verbose_name}"

    def __str__(self):
        return f"用户（{self.server.ip},{self.owner}）"
