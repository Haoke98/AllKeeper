# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/28
@Software: PyCharm
@disc:
======================================="""
from simplepro.components import fields

from .server import ServerNew


class Router(ServerNew):
    adminAddress = fields.CharField(slot_text="URL", slot="prepend", max_length=255, verbose_name="管理页面访问地址",
                                    style="width:600px;")
    adminPassword = fields.PasswordInputField(max_length=32, verbose_name="管理页密码", blank=False, null=True)

    class Meta:
        verbose_name = "路由器"
        verbose_name_plural = verbose_name
