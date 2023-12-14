# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/28
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin

from ..models import MinIO


@admin.register(MinIO)
class MinIOAdmin(admin.ModelAdmin):
    list_display = ['id', 'system', 'port', 'console_port', 'updatedAt', 'createdAt', 'deletedAt']
