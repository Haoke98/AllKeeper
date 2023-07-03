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
    list_display = LIST_DISPLAY + ['owner_natural_person', 'owner_market_subject', 'name', 'isCredit', 'balance',
                                   'consumptionLimit', 'withdrawalLimit',
                                   'temporaryLimit',
                                   'left', 'toBeReturn', 'repaymentAt']
    list_filter = ['owner_natural_person', 'owner_market_subject', 'isCredit', 'repaymentAt']
    autocomplete_fields = ['owner_natural_person', 'owner_market_subject']
    date_hierarchy = 'createdAt'
    search_fields = ['name', ]
    ordering = ('repaymentAt',)

    def balance(self, obj):
        if obj.isCredit:
            return ""
        else:
            result = 0
            for i1 in Transaction.objects.filter(_from=obj).all():
                result = result - i1.value
            for i2 in Transaction.objects.filter(to=obj).all():
                result = result + i2.value
            return result

    balance.short_description = "余额"

    def left(self, obj):
        if obj.isCredit:
            result1 = obj.temporaryLimit
            for i1 in Transaction.objects.filter(_from=obj).all():
                result1 = result1 - i1.value
            resul2 = obj.consumptionLimit + obj.withdrawalLimit
            result = result1 + resul2
            return result
        else:
            return ""

    left.short_description = "可用额度"

    def toBeReturn(self, obj):
        if obj.isCredit:
            result = 0
            print(obj.name, result)
            for i1 in Transaction.objects.filter(_from=obj).all():
                result = result + i1.value
                print("          借了", i1.value, result)
            for i2 in Transaction.objects.filter(to=obj).all():
                result = result - i2.value
                print("          还了", i2.value, result)
            return result
        else:
            return ""

    toBeReturn.short_description = "待还"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'at', '_from', 'to', 'value', 'remark', 'info', 'createdAt', 'updatedAt']
    autocomplete_fields = ['_from', 'to']
    list_filter = ['to', 'remark']
    date_hierarchy = 'createdAt'
    ordering = ('-at',)
