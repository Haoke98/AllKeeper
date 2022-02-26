from django.contrib import admin
from izBasar.admin import BaseAdmin, LIST_DISPLAY
from ..models import BT


@admin.register(BT)
class BtAdmin(BaseAdmin):
    list_display = ['id', 'port', 'server', '_username', '_password', '_url', '_basicAuthUsername',
                    '_basicAuthPassword', 'updatedAt',
                    'createdAt', 'deletedAt', ]
    autocomplete_fields = ['server', 'password', 'basicAuthPassword']
    list_filter = ['server']
    list_display_links = ['port', 'server']

    def _username(self, obj):
        return BaseAdmin.username(obj.username)

    def _password(self, obj):
        return BaseAdmin.password(obj.password.password)

    def _basicAuthUsername(self, obj):
        if obj.basicAuthUsername is None:
            return None
        return BaseAdmin.username(obj.basicAuthUsername)

    def _basicAuthPassword(self, obj):
        if obj.basicAuthPassword is None:
            return None
        return BaseAdmin.password(obj.basicAuthPassword.password)

    def _url(self, obj):
        if obj.domain is None:
            if obj.path:
                return BaseAdmin.shwoUrl(f"http://{obj.server.ip}:{obj.port}/{obj.path}")
            return BaseAdmin.shwoUrl(f"http://{obj.server.ip}:{obj.port}")
        else:
            if obj.path:
                return BaseAdmin.shwoUrl(f"{obj.domain}:{obj.port}/{obj.path}")
            return BaseAdmin.shwoUrl(f"{obj.domain}:{obj.port}")
