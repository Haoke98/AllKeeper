# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/28
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin

from ..models import Device, DeviceStatus


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand', 'remark', 'createdAt', 'updatedAt', 'deletedAt']
    search_fields = ['id', 'status', 'remark', ]


@admin.register(DeviceStatus)
class DeviceStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'device', 'ip', 'errno', 'errstr', 'createdAt']
    list_filter = ['content', 'device', 'ip', 'errno', 'createdAt']
    search_fields = ['id', 'content', 'device', 'ip', 'errno', 'createdAt']
