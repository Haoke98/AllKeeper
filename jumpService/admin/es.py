from django.contrib import admin

from accountSystem.admin.base import BaseServiceAdmin
from izBasar.admin import BaseAdmin

from ..models import ElasticSearch


@admin.register(ElasticSearch)
class ElasticSearchAdmin(BaseServiceAdmin):
    list_display = ['id', 'ip', 'port', 'elasticPwd', 'kibanaPwd', 'apmPwd', 'logstashPwd', 'beatsPwd',
                    'remoteMonitoringPwd']
    list_display_links = ['id']

    def _beats_system(self, obj):
        return BaseServiceAdmin.password(obj.apmPwd)

    def ip(self, obj):
        return BaseServiceAdmin.username(obj.server.ip)

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
        'ip': {
            'width': '260px',
            'align': 'center'
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
