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
from simplepro.admin import LIST_DISPLAY

from ..models import Transaction, CapitalAccount, CapitalAccountType


@admin.register(CapitalAccountType)
class CapitalAccountTypeAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['name', 'isCredit']
    search_fields = ['name']


@admin.register(CapitalAccount)
class CapitalAccountAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['owner', 'name',
                                   'balance',
                                   'fixedLimit', 'temporaryLimit',
                                   'withdrawalLimit',
                                   'total_limit',
                                   "used_limit_percent",
                                   'left',
                                   'withdrawal',
                                   'repayment_pending', 'unbilled_repayment_pending', 'total_repayment_pending',
                                   'repaymentDate', 'billingDate'
                                   ]
    list_filter = ['owner_natural_person', 'owner_market_subject', 'ttype', 'ttype__isCredit', 'repaymentDate']
    show_selection = True
    autocomplete_fields = ['owner_natural_person', 'owner_market_subject', 'ttype']
    date_hierarchy = 'createdAt'
    search_fields = ['name', 'owner_market_subject__name', 'owner_market_subject__ucc', 'owner_natural_person__name']
    ordering = ('repaymentDate',)

    def owner(self, obj):
        if obj.owner_market_subject:
            return obj.owner_market_subject
        elif obj.owner_natural_person:
            return obj.owner_natural_person
        else:
            return ""

    owner.short_description = "户主"

    def balance(self, obj):
        if obj.ttype and obj.ttype.isCredit:
            return ""
        else:
            result = 0
            for i1 in Transaction.objects.filter(_from=obj).all():
                result = result - i1.value
            for i2 in Transaction.objects.filter(to=obj).all():
                result = result + i2.value
            return result

    balance.short_description = "余额"

    def total_limit(self, obj):
        if obj.ttype and obj.ttype.isCredit:
            return obj.fixedLimit + obj.temporaryLimit
        else:
            return ""

    total_limit.short_description = "当前总额度"

    def used_limit_percent(self, obj):
        if obj.ttype and obj.ttype.isCredit:
            a = self.total_repayment_pending(obj)
            b = self.total_limit(obj)
            if b == 0:
                return 0
            if type(a) == str or type(b) == str:
                pass
            percent = a / b * 100
            return percent
        else:
            return ""

    used_limit_percent.short_description = "已使用"

    def left(self, obj):
        if obj.ttype and obj.ttype.isCredit:
            result1 = obj.temporaryLimit
            for i1 in Transaction.objects.filter(_from=obj).all():
                result1 = result1 - i1.value
            resul2 = obj.fixedLimit + obj.withdrawalLimit
            result = result1 + resul2
            return result
        else:
            return ""

    left.short_description = "可用额度"

    def withdrawal(self, obj):
        if obj.ttype and obj.ttype.isCredit:
            return min(self.left(obj), obj.withdrawalLimit)
        else:
            return ""

    withdrawal.short_description = "可提现"

    def repayment_pending(self, obj):
        if obj.ttype and obj.ttype.isCredit:
            result = 0
            print(obj, f"出账日:{obj.billingDate}")
            for i1 in Transaction.objects.filter(_from=obj).all():
                status = ""
                if obj.billingDate:
                    if i1.at.day > obj.billingDate:
                        status = "未出账"
                    else:
                        result = result + i1.value
                        status = "已出账"
                print(f"{i1.at}, {i1.at.day}, {status} 借了", i1.value, result)
            for i2 in Transaction.objects.filter(to=obj).all():
                result = result - i2.value
                print(f"{i2.at} 还了", i2.value, result)
            return result
        else:
            return ""

    repayment_pending.short_description = "待还"

    def unbilled_repayment_pending(self, obj):
        if obj.ttype and obj.ttype.isCredit:
            result = 0
            print(obj, f"出账日:{obj.billingDate}")
            for i1 in Transaction.objects.filter(_from=obj).all():
                status = ""
                if obj.billingDate:
                    if i1.at.day > obj.billingDate:
                        status = "未出账"
                        result = result + i1.value
                    else:
                        status = "已出账"
                print(f"{i1.at}, {i1.at.day}, {status} 借了", i1.value, result)
            for i2 in Transaction.objects.filter(to=obj).all():
                result = result - i2.value
                print(f"{i2.at} 还了", i2.value, result)
            return result
        else:
            return ""

    unbilled_repayment_pending.short_description = "未出账"

    def total_repayment_pending(self, obj):
        if obj.ttype and obj.ttype.isCredit:
            result = 0
            print(obj, f"出账日:{obj.billingDate}")
            for i1 in Transaction.objects.filter(_from=obj).all():
                result = result + i1.value
                print(f"{i1.at}, 借了", i1.value, result)
            for i2 in Transaction.objects.filter(to=obj).all():
                result = result - i2.value
                print(f"{i2.at} 还了", i2.value, result)
            return result
        else:
            return ""

    total_repayment_pending.short_description = "总待还(已使用)"

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
            withdrawal_total = 0
            rp_total = 0
            urp_total = 0
            trp_total = 0
            used_limit_percent_avg = 0
            used_limit_percent_total = 0
            for qs in queryset:
                a = self.balance(qs)
                if a != "":
                    balance_total += a
                if qs.ttype and qs.ttype.isCredit:
                    left_total += self.left(qs)
                    withdrawal_total += self.withdrawal(qs)
                    rp_total += self.repayment_pending(qs)
                    urp_total += self.unbilled_repayment_pending(qs)
                    trp_total += self.total_repayment_pending(qs)
                    p = self.used_limit_percent(qs)
                    if type(p) == str:
                        pass
                    else:
                        used_limit_percent_total += p

            used_limit_percent_avg = used_limit_percent_total / len(queryset)
            fixedLimit_total = queryset.aggregate(total=Sum('fixedLimit'))['total']
            withdrawalLimit_total = queryset.aggregate(total=Sum('withdrawalLimit'))['total']
            temporaryLimit_total = queryset.aggregate(total=Sum('temporaryLimit'))['total']
            totalLimit_total = fixedLimit_total + temporaryLimit_total
            # 需要有空字符串占位
            return (
                '',  # 勾选框
                '合计',  # ID
                '',  # 账户标识
                '',  # 户主
                '',  # createdAt
                '',  # updatedAt
                "%0.2f" % balance_total,  # 余额合计
                fixedLimit_total,  # 固定额度合计
                temporaryLimit_total,  # 临时额度合计
                withdrawalLimit_total,  # 最高可提现合计
                totalLimit_total,  # 总额度合计
                "%0.2f%%(%0.2f%%)" % (trp_total / totalLimit_total * 100, used_limit_percent_avg),  # 已使用额度总百分比
                left_total,  # 可用额度合计
                withdrawal_total,  # 可提现合计
                rp_total,  # 待还合计
                urp_total,  # 未出账合计
                "%0.2f" % trp_total,  # 总待还合计
                '')

    def formatter(self, obj, field_name, value):
        if field_name == 'balance':
            if value is not None and obj.ttype and not obj.ttype.isCredit:
                return "%0.2f" % value
            else:
                return ""
        if field_name in ["fixedLimit", "withdrawalLimit", "temporaryLimit", 'left',
                          'repayment_pending', 'unbilled_repayment_pending', 'total_repayment_pending',
                          'repaymentDate', 'billingDate']:
            if value is not None and obj.ttype and obj.ttype.isCredit:
                return "%0.2f" % value
            else:
                return ""
        if field_name == "used_limit_percent":
            if value:
                return "%0.2f%%" % value
        if field_name == "name":
            if obj.ttype:
                if value:
                    return f"{obj.ttype.name}({value})"
                else:
                    return f"{obj.ttype.name}"
        return value

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
        'owner': {
            'width': '240px',
            'align': 'left',
            'fixed': 'left',
        },
        'name': {
            'min_width': '200px',
            'align': 'left',
            'fixed': 'left',
        },
        'ttype': {
            'min_width': '120px',
            'align': 'center'
        },
        'fixedLimit': {
            'min_width': '120px',
            'align': 'right'
        },
        'temporaryLimit': {
            'min_width': '130px',
            'align': 'right'
        },
        'total_limit': {
            'min_width': '130px',
            'align': 'right'
        },
        'withdrawalLimit': {
            'min_width': '120px',
            'align': 'right'
        },
        'left': {
            'min_width': '100px',
            'align': 'right'
        },
        'withdrawal': {
            'min_width': '100px',
            'align': 'right'
        },

        'balance': {
            'min_width': '120px',
            'align': 'right'
        },
        'repayment_pending': {
            'min_width': '100px',
            'align': 'right'
        },
        'unbilled_repayment_pending': {
            'min_width': '100px',
            'align': 'right'
        },
        'total_repayment_pending': {
            'min_width': '120px',
            'align': 'right'
        },
        'repaymentDate': {
            'min_width': '120px',
            'align': 'center'
        },
        'billingDate': {
            'min_width': '120px',
            'align': 'center'
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
            'min_width': '68px',
            'align': 'center'
        },
        'at': {
            'min_width': '180px',
            'align': 'center'
        },
        '_from': {
            'min_width': '280px',
            'align': 'left'
        },
        'to': {
            'min_width': '280px',
            'align': 'left'
        },
        'value': {
            'min_width': '160px',
            'align': 'right'
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
