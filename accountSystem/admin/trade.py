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
                                   'consumptionLimit', 'withdrawalLimit', 'temporaryLimit',
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

    # 动态统计，Simple Pro独有功能
    def get_summaries(self, request, queryset):
        # 自定义统计，可以根据request的页面 来统计当前页的数据，queryset 为深拷贝对象，如果传入的话 可能会影响列表的数据
        # 返回的数据 为数组，对应列表的每一列
        # 不支持html

        # 如果想根据人员权限来动态展示，可以直接返回不同的数组，或者返回为None，为None的时候，不显示统计列

        # 如果想统计满足当前搜索条件的数据的话 ，可以直接使用queryset.来进行统计
        if request.POST.get('current_page') == '2':
            return None
        else:
            # 需要有空字符串占位
            return ('合计', '', '', '', '', '', '', '', '1', '12', '123', '1234', '12345', '123456', '')

    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '40px',
            'align': 'center'
        },
        'createdAt': {
            'width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'width': '180px',
            'align': 'left'
        },
        'owner_natural_person': {
            'width': '160px',
            'align': 'left'
        },
        'owner_market_subject': {
            'width': '240px',
            'align': 'left'
        },
        'name': {
            'width': '160px',
            'align': 'left'
        },
        'isCredit': {
            'width': '160px',
            'align': 'left'
        },
        'consumptionLimit': {
            'width': '120px',
            'align': 'left'
        },
        'withdrawalLimit': {
            'width': '120px',
            'align': 'left'
        },
        'temporaryLimit': {
            'width': '130px',
            'align': 'left'
        },
        'douyin': {
            'width': '120px',
            'align': 'left'
        },
        'license_plate_number': {
            'width': '120px',
            'align': 'left'
        },
        'repaymentAt': {
            'width': '180px',
            'align': 'left'
        }
    }


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'at', '_from', 'to', 'value', 'remark', 'info', 'createdAt', 'updatedAt']
    autocomplete_fields = ['_from', 'to']
    list_filter = ['to', 'remark']
    date_hierarchy = 'createdAt'
    ordering = ('-at',)
