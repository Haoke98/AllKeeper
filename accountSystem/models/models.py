from django.db import models

# Create your models here.


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


