# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/15
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.components import fields

from .service import AbstractBaseServiceUserModel, AbstractBaseServiceModel
from .. import ServerNew


class SSHService(AbstractBaseServiceModel):
    server = models.ForeignKey(to=ServerNew, on_delete=models.CASCADE, verbose_name="服务器", null=True,
                               blank=False, db_index=True, related_name="SSHServices")

    class Meta:
        verbose_name = "SSH服务"
        verbose_name_plural = verbose_name


class SSHServiceUser(AbstractBaseServiceUserModel):
    service = fields.ForeignKey(to=SSHService, on_delete=models.CASCADE, verbose_name="所属服务", null=True,
                                blank=False)
    userGroup = (
        (0, "root:x:0:"),
        (1, "bin:x:1:"),
        (2, "daemon:x:2:"),
        (3, "sys:x:3:"),
        (4, "adm:x:4:"),
        (5, "tty:x:5:"),
        (6, "disk:x:6:"),
        (7, "lp:x:7:"),
        (8, "mem:x:8:"),
        (9, "kmem:x:9:"),
        (10, "wheel:x:10:"),
        (11, "cdrom:x:11:"),
        (12, "mail:x:12:postfix"),
        (13, "man:x:15:"),
        (14, "dialout:x:18:"),
        (15, "floppy:x:19:"),
        (16, "games:x:20:"),
        (17, "tape:x:33:"))
    group = fields.IntegerField(verbose_name='用户组', choices=userGroup, null=True, blank=True)

    class Meta:
        verbose_name = "SSH账号"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"用户（{self.service.server},{self.owner}）"
