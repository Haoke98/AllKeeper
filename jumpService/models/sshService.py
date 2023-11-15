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

from .baseService import BaseServiceModel, BaseServiceUserModel


class SSHService(BaseServiceModel):
    class Meta:
        verbose_name = "SSH服务"
        verbose_name_plural = verbose_name


class SSHServiceUser(BaseServiceUserModel):
    service = models.ForeignKey(to=SSHService, on_delete=models.CASCADE, verbose_name="所属服务", null=True,
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
    username = models.CharField(max_length=32, null=True, blank=False, verbose_name="用户名")
    pwd = models.CharField(max_length=32, verbose_name="密码", null=True, blank=False)
    hasRootPriority = models.BooleanField(default=False, verbose_name="root权限", blank=True)
    # 密码输入框
    f3 = fields.CharField(verbose_name='测试字段（非必填）', placeholder='请输入密码', max_length=128, show_password=True, null=True,
                          blank=True, show_word_limit=True, slot='prepend', slot_text='密码')

    class Meta:
        verbose_name = "服务器用户"
        verbose_name_plural = f"所有{verbose_name}"

    def __str__(self):
        return f"用户（{self.server.ip},{self.owner}）"
