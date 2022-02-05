from django.db import models

from izBasar.models import BaseModel


class Type(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="名称", default="未知类型")
    url = models.URLField(verbose_name="网站地址", null=True, blank=True)
    icon = models.ImageField(verbose_name="图标", null=True, blank=True)

    class Meta:
        verbose_name = "账号类型"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return "%s" % self.name
