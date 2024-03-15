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

from jumpService.models import Channel


@admin.register(Channel)
class ChannelAdmin(BaseAdmin):
    list_display = ['id', 'left', 'right']
    list_filter = ['left', 'right']
    # TODO: 得列出每一段所在的网络
