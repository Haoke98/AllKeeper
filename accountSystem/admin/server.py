from django.contrib import admin

from izBasar.admin import BaseAdmin
from ..forms import ServerForm
from ..models import Server


@admin.register(Server)
class ServerAdmin(BaseAdmin):
    list_display = ["id", "ip", 'system', 'rootPassword', 'ssh', 'bios', 'group', 'hoster', 'remark',
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
        if field_name == "url":
            if value:
                return f"""<a href="{value}" target="_blank">点击跳转</a>"""
        if field_name == "name":
            if value:
                return f'''<el-button type="info" onclick="goToDetail(this)" round>{value}</el-button>'''
        return value

    fields_options = {
        'id': {
            'fixed': 'left',
            'min_width': '80px',
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
            'min_width': '248px',
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
        'remark': {
            'min_width': '200px',
            'align': 'left'
        },

        'bios': {
            'min_width': '180',
            'align': 'center'
        }
    }
