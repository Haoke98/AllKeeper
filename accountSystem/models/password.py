from django.db import models

from izBasar.models import BaseModel


class Password(BaseModel):
    password = models.CharField(max_length=36, verbose_name="密码", unique=True)

    class Meta:
        verbose_name = "密码"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return "密码：%s" % self.password
