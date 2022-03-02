from django.contrib import admin

from .base import BaseServiceAdmin
from ..models import ElasticSearch


@admin.register(ElasticSearch)
class ElasticSearchAdmin(BaseServiceAdmin):
    list_display = ['id', 'ip', 'port', '_elastic', '_kibana_system', '_apm_system']
    list_display_links = ['id']

    def _elastic(self, obj):
        return BaseServiceAdmin.password(obj.elasticPwd)

    def _kibana_system(self, obj):
        return BaseServiceAdmin.password(obj.kibanaPwd)

    def _apm_system(self, obj):
        return BaseServiceAdmin.password(obj.apmPwd)

    def _beats_system(self, obj):
        return BaseServiceAdmin.password(obj.apmPwd)

    def ip(self, obj):
        return BaseServiceAdmin.username(obj.server.ip)
