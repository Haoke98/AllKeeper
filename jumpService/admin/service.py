# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/28
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin

from ..models import Service, ServiceUser


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'server', 'port', 'updatedAt', 'createdAt', 'deletedAt']
    search_fields = ['server','port']


@admin.register(ServiceUser)
class ServiceUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'username']
