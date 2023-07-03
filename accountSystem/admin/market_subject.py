# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/6/30
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin

from ..models import MarketSubject


@admin.register(MarketSubject)
class MarketSubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'ucc', 'name', 'info', 'createdAt', 'updatedAt']
    search_fields = ['ucc', 'name']
    autocomplete_fields = []
    list_filter = []
    date_hierarchy = 'createdAt'
    ordering = ()
