from django.db import models
from simplepro.models import BaseModel

from .human import Human
from .server import Server


class BaseAccountModel(BaseModel):
    remark = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True, db_index=True)

    class Meta:
        abstract = True


class BaseServiceModel(BaseAccountModel):
    server = models.ForeignKey(to=Server, on_delete=models.CASCADE, verbose_name="服务器", null=True,
                               blank=False, db_index=True)
    port = models.PositiveIntegerField(verbose_name="端口", default=8888, blank=False, db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"服务({self.server.ip}:{self.port}）"


class BaseServiceUserModel(BaseModel):
    owner = models.ForeignKey(verbose_name="所属个体/组织", to=Human, on_delete=models.CASCADE, null=True, blank=True)
    server = models.ForeignKey(to=BaseServiceModel, on_delete=models.CASCADE, verbose_name="服务", null=True,
                               blank=False)
    username = models.CharField(max_length=32, null=True, blank=False, verbose_name="用户名")
    password = models.CharField(max_length=32, null=True, blank=False, verbose_name="密码")
    hasRootPriority = models.BooleanField(default=False, verbose_name="拥有root权限", blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"用户（{self.server.server.ip},{self.owner}）"
