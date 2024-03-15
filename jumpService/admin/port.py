# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/15
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin
from simplepro.admin import BaseAdmin

from jumpService.models import PortMap, Port


@admin.register(PortMap)
class PortMapAdmin(BaseAdmin):
    list_display = ['id', 'left', 'leftPort', 'right', 'rightPort', 'updatedAt', 'createdAt', 'deletedAt']
    list_filter = ['left', 'leftPort', 'right', 'rightPort', ]
    ordering = ['-updatedAt']
    # TODO: 得列出每一段所在的网络


@admin.register(Port)
class PortAdmin(BaseAdmin):
    list_display = ['id', 'host', 'num', 'updatedAt', 'createdAt', 'deletedAt']
    list_filter = ['host', 'num', ]
    ordering = ['-updatedAt']
