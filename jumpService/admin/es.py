from django.contrib import admin
from simplepro.admin import BaseAdmin

from .base import BaseServiceAdmin
from ..models import ElasticSearch


@admin.register(ElasticSearch)
class ElasticSearchAdmin(BaseServiceAdmin):
    list_display = ['id', 'port', 'elasticPwd', '_url', 'kibanaPwd', 'apmPwd', 'logstashPwd', 'beatsPwd',
                    'remoteMonitoringPwd']
    list_filter = []

    def _beats_system(self, obj):
        return BaseServiceAdmin.password(obj.apmPwd)

    def _url(self, obj):
        res = ""
        ips = obj.server.ips.all()
        for i, ipObj in enumerate(ips):
            print(obj.server, ipObj.ip)
            uri = "http://"
            uri += f"{ipObj.ip}:{obj.port}"
            if len(ips) == 1:
                res += f"""<a target="_blank" href="{uri}" >入口</a>"""
            else:
                res += f"""<a target="_blank" href="{uri}" >入口{i}</a></br>"""
        return res

    _url.short_description = "入口"

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "elasticPwd":
            if value:
                return BaseAdmin.password(obj.elasticPwd)
        if field_name == 'kibanaPwd':
            if value:
                return BaseAdmin.password(obj.kibanaPwd)
        if field_name == "apmPwd":
            if value:
                return BaseAdmin.password(obj.apmPwd)
        if field_name == "logstashPwd":
            if value:
                return BaseAdmin.password(obj.logstashPwd)
        if field_name == "beatsPwd":
            if value:
                return BaseAdmin.password(obj.beatsPwd)
        if field_name == "remoteMonitoringPwd":
            if value:
                return BaseAdmin.password(obj.remoteMonitoringPwd)
        return value

    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '70px',
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
        'server': {
            'width': '260px',
            'align': 'left'
        },
        'port': {
            'width': '120px',
            'align': 'center'
        },
        'elasticPwd': {
            'width': '200px',
            'align': 'left'
        },
        'kibanaPwd': {
            'width': '200px',
            'align': 'left'
        },
        'apmPwd': {
            'width': '200px',
            'align': 'left'
        },
        'logstashPwd': {
            'width': '200px',
            'align': 'left'
        },
        'beatsPwd': {
            'width': '200px',
            'align': 'left'
        },
        'remoteMonitoringPwd': {
            'width': '240px',
            'align': 'left'
        }
    }
