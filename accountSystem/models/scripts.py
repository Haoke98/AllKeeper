from django.db import models
from simplepro.models import BaseModel


class Script(BaseModel):
    name = models.CharField(max_length=50, verbose_name="名称", default="未知脚本")
    content = models.TextField(verbose_name="内容", null=False)

    class Meta:
        verbose_name = "脚本"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return self.name
