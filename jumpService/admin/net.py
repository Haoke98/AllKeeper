# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/27
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin

from ..models import NetModel


@admin.register(NetModel)
class NetAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'remark', 'createdAt', 'updatedAt', 'deletedAt']
    search_fields = ['content', 'remark']
