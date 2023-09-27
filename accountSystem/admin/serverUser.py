from django.contrib import admin

from izBasar.admin import LIST_DISPLAY, BaseAdmin
from ..forms import ServerUserForm
from ..models import ServerUser


@admin.register(ServerUser)
class ServerUserAdmin(BaseAdmin):
    list_display = LIST_DISPLAY + ['username', 'pwd', 'hasRootPriority', '_ip', 'owner']
    autocomplete_fields = ['server', 'owner']
    list_filter = ['hasRootPriority', 'server', 'owner']
    list_select_related = autocomplete_fields
    form = ServerUserForm

    def _ip(self, obj):
        return BaseAdmin.username(obj.server.ip)

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
            'min_width': '220px',
            'align': 'center'
        },
        'username': {
            'min_width': '220px',
            'align': 'center'
        },
        'pwd': {
            'min_width': '180px',
            'align': 'left'
        },
        'hasRootPriority': {
            'min_width': '100px',
            'align': 'center'
        },
        'owner': {
            'min_width': '280px',
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


class ServerUserInlineAdmin(admin.TabularInline):
    model = ServerUser
    form = ServerUserForm
    autocomplete_fields = ['server', 'owner']
    min_num = 0
    extra = 0
