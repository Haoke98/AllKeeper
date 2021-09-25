from django.db import models

# Create your models here.
from accountSystem.models.base import BaseModel


class PPassword(BaseModel):
    password = models.CharField(max_length=20, verbose_name="密码", unique=True)

    class Meta:
        verbose_name = "密码"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return "密码：%s" % self.password


class TTel(BaseModel):
    content = models.CharField(max_length=11, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "手机号"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        if self.remark is None:
            return "%s" % self.content
        else:
            return "%s(%s)" % (self.content, self.remark)


class EEmail(BaseModel):
    content = models.EmailField(null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "电子邮箱"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        if self.remark is None:
            return "%s" % self.content
        else:
            return "%s(%s)" % (self.content, self.remark)


class Group(BaseModel):
    name = models.CharField(max_length=50, verbose_name="名称", default="未知组")

    class Meta:
        verbose_name = "账号集"
        verbose_name_plural = "所有" + verbose_name

    def __str__(self):
        return "所有%s账号" % self.name
