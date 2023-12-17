# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/28
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin
from simplepro.admin import FieldOptions

from ..models import MinIO


@admin.register(MinIO)
class MinIOAdmin(admin.ModelAdmin):
    list_display = ['id', 'system', 'port', 'console_port', 'updatedAt', 'createdAt', 'deletedAt']


    fields_options = {
        'id': FieldOptions.UUID,
        'code': {
            'min_width': '88px',
            'align': 'center'
        },
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'system': {
            'min_width': '320px',
            'align': 'center'
        },
        'net': FieldOptions.IP_ADDRESS,
        'image': {
            'min_width': '160px',
            'align': 'center'
        },
        'rootUsername': {
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
        'server': {
            'min_width': '220px',
            'align': 'left'
        },
        'status': {
            'min_width': '180px',
            'align': 'left'
        },
        'remark': FieldOptions.REMARK,
        'bios': {
            'min_width': '180',
            'align': 'center'
        },
        'cabinet': {
            'min_width': '180',
            'align': 'center'
        },
        'mac': FieldOptions.MAC_ADDRESS
    }
