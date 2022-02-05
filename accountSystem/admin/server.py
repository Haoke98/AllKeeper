from django.contrib import admin
from ..models import Server
from izBasar.admin import LIST_DISPLAY, BaseAdmin
from .serverUser import ServerUserInlineAdmin


@admin.register(Server)
class ServerAdmin(BaseAdmin):
    list_display = LIST_DISPLAY + ["_ip", '_password', 'remark', 'group',
                                   'hoster']
    list_display_links = ['id', 'remark', 'group', 'hoster']
    list_filter = ['group', 'hoster']
    date_hierarchy = 'updatedAt'
    search_fields = ['ip', 'rootPwd.password',
                     'remark', 'hoster']
    search_help_text = ['你好，这是搜索帮助语句！']
    autocomplete_fields = ['rootPwd', 'group']
    inlines = [ServerUserInlineAdmin]

    def _ip(self, obj):
        return BaseAdmin.username(obj.ip)

    def _password(self, obj):
        return BaseAdmin.password(obj.rootPwd.password)

    _password.short_description = "root密码"
