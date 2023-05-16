# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/5/15
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin

from ..models import BreathInfo


@admin.register(BreathInfo)
class BreathInfoAdmin(admin.ModelAdmin):
    list_display = ["id", "createdAt", "updatedAt", "accessAt", "ip", "mac", "latitude", "longitude"]
