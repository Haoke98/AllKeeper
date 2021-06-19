from django.db import models

# Create your models here.
from miniProgram.models import MyModel


class PPassword(models.Model):
    password = models.CharField(max_length=20, verbose_name="密码", unique=True)

    def __str__(self):
        return "密码：%s" % self.password


class TTel(models.Model):
    content = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return self.content


class EEmail(models.Model):
    content = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.content


class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="名称", default="未知组")

    def __str__(self):
        return "所有%s账号" % self.name


class Account(MyModel):
    name = models.CharField(max_length=50, verbose_name="账号归属", default="未知账号")
    username = models.CharField(max_length=40, verbose_name="用户名")
    password = models.ForeignKey(to=PPassword, on_delete=models.CASCADE, verbose_name="密码", null=True)
    tel = models.ForeignKey(verbose_name="绑定的手机号", to=TTel, on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField(verbose_name="网站地址", null=True, blank=True)
    email = models.ForeignKey(verbose_name="关联邮箱", to=EEmail, on_delete=models.CASCADE, null=True, blank=True)
    Introduce = models.TextField(verbose_name="说明", null=True, blank=True)
    group = models.ForeignKey(verbose_name="所属账号组", to=Group, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "%s账号" % self.name
