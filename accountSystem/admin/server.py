from django.contrib import admin

from izBasar.admin import BaseAdmin
from .serverUser import ServerUserInlineAdmin
from ..forms import ServerForm
from ..models import Server


@admin.register(Server)
class ServerAdmin(BaseAdmin):
    list_display = ["id", "_ip", '_password', 'ssh', '_biosPassword', 'remark', 'group', 'hoster', "createdAt",
                    "updatedAt",
                    "deletedAt", ]
    list_display_links = ['id', 'remark', 'group', 'hoster']
    list_filter = ['group', 'hoster', 'ssh']
    date_hierarchy = 'updatedAt'
    search_fields = ['ip', 'remark', 'hoster']
    search_help_text = ['你好，这是搜索帮助语句！']
    autocomplete_fields = ['group']
    form = ServerForm
    inlines = [ServerUserInlineAdmin]

    def _ip(self, obj):
        return BaseAdmin.username(obj.ip)

    def _password(self, obj):
        return BaseAdmin.password(obj.rootPassword)

    _password.short_description = "root密码"

    def _biosPassword(self, obj):
        return BaseAdmin.password(obj.bios)

    _biosPassword.short_description = "BIOS密码"


    class Media:

        def __init__(self):
            pass

        css = {
        }
        js = [
            'kindeditor4.1.11/kindeditor-all.js',
            'kindeditor4.1.11/lang/zh-CN.js',

            'js/server-admin-kind-editor-config.js',
        ]

