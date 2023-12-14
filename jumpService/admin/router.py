# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/28
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin

from .net import IPAddressInlineAdmin
from ..models import Router


@admin.register(Router)
class RouterAdmin(admin.ModelAdmin):
    list_display = ['code',
                    'adminAddress', 'adminPassword', 'rootPassword', 'status', 'remark', 'bios', 'hoster',
                    "updatedAt", "createdAt", "deletedAt", 'id']
    inlines = [IPAddressInlineAdmin]
    fields_options = {
        'id': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'code': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'createdAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'deletedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'ip': {
            'min_width': '200px',
            'align': 'center'
        },
        'net': {
            'min_width': '180px',
            'align': 'center'
        },
        'system': {
            'min_width': '160px',
            'align': 'center'
        },
        'adminPassword': {
            'min_width': '180px',
            'align': 'center'
        },
        'rootPassword': {
            'min_width': '180px',
            'align': 'center'
        },
        'ssh': {
            'min_width': '120px',
            'align': 'center'
        },
        'hoster': {
            'min_width': '320px',
            'align': 'left'
        },
        'group': {
            'min_width': '220px',
            'align': 'left'
        },
        'status': {
            'min_width': '180px',
            'align': 'left'
        },
        'adminAddress': {
            'min_width': '200px',
            'align': 'left'
        },
        'remark': {
            'min_width': '200px',
            'align': 'left'
        },

        'bios': {
            'min_width': '180',
            'align': 'center'
        }
    }
