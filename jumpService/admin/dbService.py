from django.contrib import admin
from simplepro.admin import BaseAdmin

from .dbServiceUser import DbServiceUserInlineAdmin
from ..forms import DbServiceForm
from ..models import DbService


@admin.register(DbService)
class DbServiceAdmin(BaseAdmin):
    form = DbServiceForm
    list_display = ['id', 'server', 'port', '_username', 'pwd', 'ttype', 'remark', 'updatedAt', 'createdAt']
    list_display_links = ['createdAt', 'updatedAt', 'server', 'port', 'ttype']
    list_filter = ['server', 'port', 'ttype']
    date_hierarchy = 'updatedAt'
    search_fields = ['server__ip', 'port', 'ttype', 'remark', ]
    search_help_text = ['你好，这是搜索帮助语句！']
    autocomplete_fields = ['server']
    inlines = [DbServiceUserInlineAdmin]

    def _username(self, obj):
        username = 'root'
        if obj.ttype == 1:
            username = 'postgres'
        return BaseAdmin.username(username)

    _username.short_description = "用户名"

    def formatter(self, obj, field_name, value):
        if field_name == 'pwd':
            if value:
                return BaseAdmin.password(obj.pwd)
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
        'server': {
            'min_width': '320px',
            'align': 'left'
        },
        'port': {
            'min_width': '140px',
            'align': 'center'
        },
        '_username': {
            'min_width': '200px',
            'align': 'left'
        },
        'pwd': {
            'min_width': '180px',
            'align': 'center'
        },
        'ttype': {
            'min_width': '178px',
            'align': 'center'
        },
        'remark': {
            'width': '200px',
            'align': 'left'
        }
    }
