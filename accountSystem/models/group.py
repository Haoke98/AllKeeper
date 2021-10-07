from django.db import models

from izBasar.models import BaseModel


# Create your models here.

class Group(BaseModel):
    name = models.CharField(max_length=50, verbose_name="名称", default="未知组")

    class Meta:
        verbose_name = "账号集"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return "所有%s账号" % self.name
