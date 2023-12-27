# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/12/27
@Software: PyCharm
@disc:
======================================="""
from simplepro.admin import BaseAdmin


class BaseServiceAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['server', 'port']
    autocomplete_fields = ['system']
    list_select_related = ['server']
