from django.contrib import admin

from izBasar.admin import BaseAdmin
from ..models import Server, ServerNew


@admin.register(Server)
class ServerAdmin(BaseAdmin):
    list_display = ['code', 'net', "ip", 'system', 'rootPassword', 'ssh', 'status', 'remark', 'bios', 'hoster',
                    "updatedAt",
                    "createdAt",
                    "deletedAt", ]
    list_display_links = ['remark', 'hoster']
    list_filter = ['hoster', 'ssh', 'system', 'net', 'status']
    date_hierarchy = 'updatedAt'
    search_fields = ['ip', 'remark', 'code']
    search_help_text = ['你好，这是搜索帮助语句！']
    autocomplete_fields = ['net']
    list_per_page = 10
    fields = ['code', 'hoster', 'net', 'ip', 'system', 'rootUsername', 'rootPassword', 'status', 'bios', 'ssh',
              'mac',
              'remark',
              'info']

    # inlines = [ServerUserInlineAdmin]

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "ip":
            if value:
                return BaseAdmin.username(obj.ip)
        if field_name == 'rootPassword':
            if value:
                return BaseAdmin.password(obj.rootPassword)
        if field_name == "bios":
            if value:
                return BaseAdmin.password(obj.bios)
        return value

    fields_options = {
        'id': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'code': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'createdAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'deletedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'ip': {
            'min_width': '200px',
            'align': 'center'
        },
        'net': {
            'min_width': '180px',
            'align': 'center'
        },
        'system': {
            'min_width': '160px',
            'align': 'center'
        },
        'rootPassword': {
            'min_width': '180px',
            'align': 'center'
        },
        'ssh': {
            'min_width': '120px',
            'align': 'center'
        },
        'hoster': {
            'min_width': '320px',
            'align': 'left'
        },
        'group': {
            'min_width': '220px',
            'align': 'left'
        },
        'status': {
            'min_width': '180px',
            'align': 'left'
        },
        'remark': {
            'min_width': '200px',
            'align': 'left'
        },

        'bios': {
            'min_width': '180',
            'align': 'center'
        }
    }


@admin.register(ServerNew)
class ServerNewAdmin(BaseAdmin):
    list_display = ['code', 'system', 'rootPassword', 'ssh', 'status', 'remark', 'bios', 'hoster',
                    "updatedAt",
                    "createdAt",
                    "deletedAt", ]
    list_display_links = ['remark', 'hoster']
    list_filter = ['hoster', 'ssh', 'system', 'status']
    date_hierarchy = 'updatedAt'
    search_fields = ['ip', 'remark', 'code']
    search_help_text = ['你好，这是搜索帮助语句！']
    autocomplete_fields = []
    list_per_page = 10
    fields = ['code', 'hoster', 'net', 'ip', 'system', 'rootUsername', 'rootPassword', 'status', 'bios', 'ssh',
              'mac',
              'remark',
              'info']

    # inlines = [ServerUserInlineAdmin]

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "ip":
            if value:
                return BaseAdmin.username(obj.ip)
        if field_name == 'rootPassword':
            if value:
                return BaseAdmin.password(obj.rootPassword)
        if field_name == "bios":
            if value:
                return BaseAdmin.password(obj.bios)
        return value

    fields_options = {
        'id': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'code': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'createdAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'deletedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'ip': {
            'min_width': '200px',
            'align': 'center'
        },
        'net': {
            'min_width': '180px',
            'align': 'center'
        },
        'system': {
            'min_width': '160px',
            'align': 'center'
        },
        'rootPassword': {
            'min_width': '180px',
            'align': 'center'
        },
        'ssh': {
            'min_width': '120px',
            'align': 'center'
        },
        'hoster': {
            'min_width': '320px',
            'align': 'left'
        },
        'group': {
            'min_width': '220px',
            'align': 'left'
        },
        'status': {
            'min_width': '180px',
            'align': 'left'
        },
        'remark': {
            'min_width': '200px',
            'align': 'left'
        },

        'bios': {
            'min_width': '180',
            'align': 'center'
        }
    }
