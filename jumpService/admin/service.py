# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/28
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin

from izBasar.admin import BaseAdmin
from ..models import Service, ServiceUser


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'remark', 'system', 'port', '_url', 'updatedAt', 'createdAt',
                    'deletedAt']
    search_fields = ['system', 'port', 'remark']
    list_filter = ['system__image', 'system__server']

    def _url(self, obj):
        res = ""
        if obj.system:
            ips = obj.system.server.ips.all()
            for i, ipObj in enumerate(ips):
                print(obj.system, ipObj.ip)
                uri = "http://"
                uri += f"{ipObj.ip}:{obj.port}"
                if len(ips) == 1:
                    res += f"""<a target="_blank" href="{uri}" >入口</a>"""
                else:
                    res += f"""<a target="_blank" href="{uri}" >入口{i}</a></br>"""
            return res
        return None

    _url.short_description = "入口"

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
        'id': {
            'min_width': '88px',
            'align': 'center',
            'fixed': 'left'
        },
        'code': {
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
        'system': {
            'min_width': '320px',
            'align': 'center'
        },
        'net': {
            'min_width': '180px',
            'align': 'center'
        },
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


@admin.register(ServiceUser)
class ServiceUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'username']

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
        'id': {
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
