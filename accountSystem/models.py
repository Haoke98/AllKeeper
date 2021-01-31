from django.db import models

# Create your models here.
from miniProgram.models import MyModel


class Password(models.Model):
    password = models.CharField(max_length=20, verbose_name="密码", unique=True)

    def __str__(self):
        return "密码：%s" % self.password


class Account(MyModel):
    name = models.CharField(max_length=50, verbose_name="账号归属", default="未知账号")
    username = models.CharField(max_length=20, verbose_name="用户名")
    password = models.ForeignKey(to=Password, on_delete=models.CASCADE, verbose_name="密码")
    url = models.URLField(verbose_name="网站地址", null=True, blank=True)
    email = models.EmailField(verbose_name="关联邮箱", null=True, blank=True)
    Introduce = models.TextField(verbose_name="说明", null=True, blank=True)

    def __str__(self):
        return "%s账号" % self.name
