# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/6/25
@Software: PyCharm
@disc:
======================================="""

from django.contrib import admin
from django.db.models import Sum

from izBasar.admin import LIST_DISPLAY
from ..models import Transaction, CapitalAccount


@admin.register(CapitalAccount)
class CapitalAccountAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['owner_natural_person', 'owner_market_subject', 'name', 'isCredit', 'balance',
                                   'consumptionLimit', 'withdrawalLimit', 'temporaryLimit',
                                   'left', 'toBeReturn', 'repaymentDate', 'billingDate']
    list_filter = ['owner_natural_person', 'owner_market_subject', 'isCredit', 'repaymentDate']
    show_selection = True
    autocomplete_fields = ['owner_natural_person', 'owner_market_subject']
    date_hierarchy = 'createdAt'
    search_fields = ['name', 'owner_market_subject__name', 'owner_market_subject__ucc', 'owner_natural_person__name']
    ordering = ('repaymentDate',)

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
            balance_total = 0
            left_total = 0
            toBeReturn_total = 0
            for qs in queryset:
                a = self.balance(qs)
                if a != "":
                    balance_total += a
                b = self.left(qs)
                if b != "":
                    left_total += b
                c = self.toBeReturn(qs)
                if c != "":
                    toBeReturn_total += c
            consumptionLimit_total = queryset.aggregate(total=Sum('consumptionLimit'))['total']
            withdrawalLimit_total = queryset.aggregate(total=Sum('withdrawalLimit'))['total']
            temporaryLimit_total = queryset.aggregate(total=Sum('temporaryLimit'))['total']

            # 需要有空字符串占位
            return (
                '合计', '', '', '', '', '', '', '', balance_total, consumptionLimit_total, withdrawalLimit_total,
                temporaryLimit_total, left_total, toBeReturn_total,
                '')

    fields_options = {
        'id': {
            'fixed': 'left',
            'min_width': '68px',
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
        'left': {
            'width': '100px',
            'align': 'left'
        },
        'toBeReturn': {
            'width': '100px',
            'align': 'left'
        },
        'repaymentDate': {
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

    fields_options = {
        'id': {
            # 'fixed': 'left',
            'width': '80px',
            'align': 'center'
        },
        'at': {
            'width': '180px',
            'align': 'left'
        },
        '_from': {
            'width': '280px',
            'align': 'center'
        },
        'to': {
            'width': '280px',
            'align': 'center'
        },
        'value': {
            'width': '160px',
            'align': 'center'
        },
        'remark': {
            'width': '100px',
            'align': 'left'
        },
        'info': {
            'width': '200px',
            'align': 'left'
        },
        'asset_date': {
            'width': '180px',
            'align': 'center'
        },
        'added_date': {
            'width': '180px',
            'align': 'center'
        },
        'thumb': {
            'width': '120px',
            'align': 'center'
        },
        'origin': {
            'width': '200px',
            'align': 'center'
        },
        'detach_icloud_date': {
            'width': '180px',
            'align': 'center'
        },
        'createdAt': {
            'width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'width': '180px',
            'align': 'left'
        }
    }
