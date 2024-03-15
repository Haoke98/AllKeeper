# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/15
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin
from ..models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remark', 'createdAt', 'updatedAt', 'deletedAt']
    search_fields = ['id', 'name', 'remark', ]
    list_filter = ['createdAt', 'updatedAt', 'deletedAt']
