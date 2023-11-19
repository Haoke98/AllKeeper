from django.contrib import admin

from izBasar.admin import BaseAdmin
from ..models import SSHServiceUser, SSHService


@admin.register(SSHService)
class SSHServiceAdmin(BaseAdmin):
    list_display = ['id', 'server', 'port', 'updatedAt', 'createdAt']
    list_filter = ['server', 'port']
    autocomplete_fields = ['server']
    search_fields = ['server__ip', 'port', 'remark']


@admin.register(SSHServiceUser)
class SSHUserAdmin(BaseAdmin):
    list_display = ['id', '_ip', 'username', 'password', 'owner', 'updatedAt', 'createdAt']
    autocomplete_fields = ['service']
    list_filter = ['hasRootPriority', 'service', 'owner']
    list_select_related = autocomplete_fields
    fields = ['owner', 'service', 'username', 'password', 'group', 'f3', 'info']

    def _ip(self, obj):
        return BaseAdmin.username(obj.server.ip)

    _ip.short_description = "服务器"

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "username":
            if value:
                return BaseAdmin.username(obj.username)
        if field_name == 'pwd':
            if value:
                return BaseAdmin.password(obj.pwd)
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
        '_ip': {
            'min_width': '280px',
            'align': 'center'
        },
        'username': {
            'min_width': '220px',
            'align': 'center'
        },
        'pwd': {
            'min_width': '200px',
            'align': 'left'
        },
        'group': {
            'min_width': '200px',
            'align': 'center'
        },
        'owner': {
            'min_width': '280px',
            'align': 'center'
        }
    }


class ServerUserInlineAdmin(admin.TabularInline):
    model = SSHServiceUser
    autocomplete_fields = ['server', 'owner']
    min_num = 0
    extra = 0
