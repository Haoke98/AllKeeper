# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/28
@Software: PyCharm
@disc:
======================================="""

from django.contrib import admin
from django.db.models import QuerySet
from simplepro.decorators import button

from izBasar.admin import BaseAdmin, FieldOptions
from ..models import Service, ServiceUser, ServiceType


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remark', 'defaultPort', 'updatedAt', 'createdAt',
                    'deletedAt']
    search_fields = []
    list_filter = []
    actions = ['migrate']

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

    @button(type='danger', short_description='数据迁移', enable=True, confirm="您确定要生成吗？")
    def migrate(self, request, queryset: QuerySet):
        # es = ElasticSearch.objects.filter()
        # for qs in queryset.all():
        #     old_id = qs.id
        #     qs.id = str(uuid.uuid4())
        #     print(old_id, ">>>", qs.id)
        #     qs.save()
        #     Service.objects.filter(id=old_id).delete()
        # qs.save()
        return {
            'state': True,
            'msg': f'迁移完成'
        }


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', '_type', 'system', 'port', '_url', 'remark', 'updatedAt', 'createdAt',
                    'deletedAt']
    search_fields = ['system', 'port', 'remark']
    list_filter = ['_type', 'system__image', 'system__server']
    actions = ['migrate']

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
        '_type': {
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

    @button(type='danger', short_description='数据迁移', enable=True, confirm="您确定要生成吗？")
    def migrate(self, request, queryset: QuerySet):
        # es = ElasticSearch.objects.filter()
        # for qs in queryset.all():
        #     old_id = qs.id
        #     qs.id = str(uuid.uuid4())
        #     print(old_id, ">>>", qs.id)
        #     qs.save()
        #     Service.objects.filter(id=old_id).delete()
        # qs.save()
        return {
            'state': True,
            'msg': f'迁移完成'
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
