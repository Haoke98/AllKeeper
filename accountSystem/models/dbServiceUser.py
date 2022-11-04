from django.db import models

from .base import BaseServiceUserModel
from .dbService import DbService
from .human import Human


class DbServiceUser(BaseServiceUserModel):
    server = models.ForeignKey(to=DbService, on_delete=models.CASCADE, verbose_name="服务器", null=True,
                               blank=False)

    class Meta:
        verbose_name = "数据库用户"
        verbose_name_plural = f"所有{verbose_name}"

    def __str__(self):
        return f"用户（{self.server.server.ip},{self.owner}）"
