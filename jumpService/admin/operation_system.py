# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/12/11
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin

from izBasar.admin import BaseAdmin, FieldOptions
from ..models import OperationSystem, OperationSystemImage


@admin.register(OperationSystemImage)
class OperationSystemImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'createdAt', 'updatedAt', 'name', 'version', 'deletedAt']


@admin.register(OperationSystem)
class OperationSystemAdmin(admin.ModelAdmin):
    list_display = ['id', 'createdAt', 'updatedAt', 'image', 'server', 'rootUsername', 'rootPassword', 'deletedAt']
    list_filter = ['image', 'server']
    search_fields = ['image', 'server']

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "ip":
            if value:
                return BaseAdmin.username(obj.ip)
        if field_name == 'rootPassword':
            if value:
                return BaseAdmin.password(obj.rootPassword)
        if field_name == "bios":
            if value:
                return BaseAdmin.password(obj.bios)
        return value

    fields_options = {
        'id': FieldOptions.UUID,
        'code': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'server': {
            'min_width': '280px',
            'align': 'left'
        },
        'net': {
            'min_width': '180px',
            'align': 'center'
        },
        'image': {
            'min_width': '160px',
            'align': 'left'
        },
        'rootUsername': FieldOptions.USER_NAME,
        'rootPassword': FieldOptions.PASSWORD,
        'ssh': {
            'min_width': '120px',
            'align': 'center'
        },
        'hoster': {
            'min_width': '320px',
            'align': 'left'
        },
        'status': {
            'min_width': '180px',
            'align': 'left'
        },
        'remark': {
            'min_width': '200px',
            'align': 'left'
        },

        'bios': {
            'min_width': '180',
            'align': 'center'
        },
        'cabinet': {
            'min_width': '180',
            'align': 'center'
        },
        'mac': {
            'min_width': '220px',
            'align': 'left'
        }
    }
