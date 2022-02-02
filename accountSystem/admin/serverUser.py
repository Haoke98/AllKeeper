from django.contrib import admin
from izBasar.admin import LIST_DISPLAY, BaseAdmin
from ..models import ServerUser


@admin.register(ServerUser)
class ServerUserAdmin(BaseAdmin):
    list_display = LIST_DISPLAY + ['_username', '_password', 'hasRootPriority', '_ip', 'owner']
    autocomplete_fields = ['password', 'server', 'owner']
    list_filter = ['hasRootPriority', 'server', 'owner']
    list_select_related = autocomplete_fields

    def _username(self, obj):
        return BaseAdmin.username(obj.username)

    def _password(self, obj):
        return BaseAdmin.password(obj.password.password)

    _password.short_description = "密码"

    def _ip(self, obj):
        return BaseAdmin.username(obj.server.ip)


class ServerUserInlineAdmin(admin.TabularInline):
    model = ServerUser
    autocomplete_fields = ['password', 'server', 'owner']
    min_num = 0
    extra = 0
