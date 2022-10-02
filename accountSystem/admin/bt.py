from django.contrib import admin

from izBasar.admin import BaseAdmin
from ..models import BT


@admin.register(BT)
class BtAdmin(BaseAdmin):
    list_display = ['id', 'port', 'server', '_username', '_password', '_url', '_basicAuthUsername',
                    '_basicAuthPassword', 'updatedAt',
                    'createdAt', 'deletedAt', ]
    autocomplete_fields = ['server']
    list_filter = ['server']
    list_display_links = ['port', 'server']

    def _username(self, obj):
        return BaseAdmin.username(obj.username)

    def _password(self, obj):
        return BaseAdmin.password(obj.pwd)

    def _basicAuthUsername(self, obj):
        if obj.basicAuthUsername is None:
            return None
        return BaseAdmin.username(obj.basicAuthUsername)

    def _basicAuthPassword(self, obj):
        if obj.basicAuthPwd is None:
            return None
        return BaseAdmin.password(obj.basicAuthPwd)

    def _url(self, obj):
        uri = "http://"
        if obj.basicAuthUsername and obj.basicAuthPwd:
            uri += f"{obj.basicAuthUsername}:{obj.basicAuthPwd}@"
        if obj.domain:
            uri += obj.domain
        else:
            uri += obj.server.ip
        uri += f":{obj.port}"
        if obj.path:
            uri += f"/{obj.path}"
        return BaseAdmin.shwoUrl(uri)
