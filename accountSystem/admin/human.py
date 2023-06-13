# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/6/13
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin

from izBasar.admin import LIST_DISPLAY
from ..models import Human, Account


@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ["name", 'idCardNum', 'sex', '_count', 'info']
    search_fields = ['name', 'idCardNum']
    list_filter = ['sex']
    list_per_page = 14

    def _count(self, obj):
        return Account.objects.filter(types=obj.id).count()

    _count.short_description = "所关联的账号数量"
