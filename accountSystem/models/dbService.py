from django.db import models

from .base import BaseServiceModel


class DbService(BaseServiceModel):
    pwd = models.CharField(verbose_name="root密码", max_length=48, null=True, blank=True)

    class Meta:
        verbose_name = "数据服务"
        verbose_name_plural = f"所有{verbose_name}"

    def __str__(self):
        return f"数据{super().__str__()}"
