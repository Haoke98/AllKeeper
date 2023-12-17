# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/2/19
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin
from simplepro.admin import BaseAdmin

from accountSystem.models import Script


@admin.register(Script)
class ScriptAdmin(BaseAdmin):
    list_display = ['id', 'name', 'content', 'updatedAt', 'createdAt', 'deletedAt', ]
