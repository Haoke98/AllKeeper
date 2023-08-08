from django.contrib import admin

from izBasar.admin import BaseAdmin
from ..forms import ServerForm
from ..models import Server


@admin.register(Server)
class ServerAdmin(BaseAdmin):
    list_display = ["id", "_ip", 'system', '_password', 'ssh', '_biosPassword', 'group', 'hoster', 'remark',
                    "createdAt",
                    "updatedAt",
                    "deletedAt", ]
    list_display_links = ['id', 'remark', 'group', 'hoster']
    list_filter = ['group', 'hoster', 'ssh', 'system']
    date_hierarchy = 'updatedAt'
    search_fields = ['ip', 'remark']
    search_help_text = ['你好，这是搜索帮助语句！']
    autocomplete_fields = ['group']
    form = ServerForm
    list_per_page = 10
    # inlines = [ServerUserInlineAdmin]

    def _ip(self, obj):
        return BaseAdmin.username(obj.ip)

    _ip.short_description = "IP地址"

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
        ]

    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '40px',
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
        '_ip': {
            'width': '140px',
            'align': 'center'
        },
        'system': {
            'width': '160px',
            'align': 'center'
        },
        'ssh': {
            'width': '120px',
            'align': 'center'
        },
        'hoster': {
            'width': '320px',
            'align': 'left'
        },
        'group': {
            'width': '220px',
            'align': 'left'
        },
        '_password': {
            'width': '80px',
            'align': 'center'
        },
        'remark': {
            'width': '200px',
            'align': 'left'
        },

        '_biosPassword': {
            'width': '100',
            'align': 'center'
        }
    }
