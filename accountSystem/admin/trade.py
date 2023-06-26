# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/6/25
@Software: PyCharm
@disc:
======================================="""

from django.contrib import admin

from izBasar.admin import LIST_DISPLAY
from ..models import Transaction, CapitalAccount


@admin.register(CapitalAccount)
class CapitalAccountAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['name', 'owner', 'balance']
    list_filter = ['owner']
    autocomplete_fields = ['owner']
    date_hierarchy = 'createdAt'
    search_fields = ['name', 'owner__name']
    # list_filter = ['paid_off', 'whose', 'ddl']
    # ordering = ('ddl',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'at', '_from', 'to', 'value', 'info', 'createdAt', 'updatedAt']
    list_filter = ['_from', 'to']
    autocomplete_fields = ['_from', 'to']
    date_hierarchy = 'createdAt'
    # ordering = ('ddl',)
