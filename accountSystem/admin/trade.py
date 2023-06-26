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
    list_display = LIST_DISPLAY + ['name', 'owner', 'balance', 'left']
    list_filter = ['owner']
    autocomplete_fields = ['owner']
    date_hierarchy = 'createdAt'
    search_fields = ['name', 'owner__name']

    def left(self, obj):
        result = obj.balance
        all1 = Transaction.objects.filter(_from=obj).all()
        all2 = Transaction.objects.filter(to=obj).all()
        for i1 in all1:
            result = result - i1.value
        for i2 in all2:
            result = result + i2.value
        return result

    left.short_description = "可用余额"
    # ordering = ('ddl',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'at', '_from', 'to', 'value', 'remark', 'info', 'createdAt', 'updatedAt']
    autocomplete_fields = ['_from', 'to']
    list_filter = ['to__owner', 'to', 'remark']
    date_hierarchy = 'createdAt'
    # ordering = ('ddl',)
