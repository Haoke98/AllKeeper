from django.db import models

# Create your models here.
from accountSystem.models.base import BaseModel


class PPassword(BaseModel):
    password = models.CharField(max_length=20, verbose_name="密码", unique=True)

    def __str__(self):
        return "密码：%s" % self.password


class TTel(BaseModel):
    content = models.CharField(max_length=11, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.content


class EEmail(BaseModel):
    content = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.content


class Group(BaseModel):
    name = models.CharField(max_length=50, verbose_name="名称", default="未知组")

    def __str__(self):
        return "所有%s账号" % self.name


