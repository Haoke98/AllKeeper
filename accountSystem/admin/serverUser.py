from django.contrib import admin

from izBasar.admin import LIST_DISPLAY, BaseAdmin
from ..forms import ServerUserForm
from ..models import ServerUser


@admin.register(ServerUser)
class ServerUserAdmin(BaseAdmin):
    list_display = LIST_DISPLAY + ['_username', '_password', 'hasRootPriority', '_ip', 'owner']
    autocomplete_fields = ['server', 'owner']
    list_filter = ['hasRootPriority', 'server', 'owner']
    list_select_related = autocomplete_fields
    form = ServerUserForm

    def _username(self, obj):
        return BaseAdmin.username(obj.username)

    def _password(self, obj):
        return BaseAdmin.password(obj.pwd)

    _password.short_description = "密码"

    def _ip(self, obj):
        return BaseAdmin.username(obj.server.ip)


class ServerUserInlineAdmin(admin.TabularInline):
    model = ServerUser
    form = ServerUserForm
    autocomplete_fields = ['server', 'owner']
    min_num = 0
    extra = 0
