from django.contrib import admin
from ..models import DbServer
from izBasar.admin import LIST_DISPLAY, BaseAdmin
from .dbServerUser import DbServerUserInlineAdmin


@admin.register(DbServer)
class DbServerAdmin(BaseAdmin):
    list_display = LIST_DISPLAY + ['server', '_password', 'remark', ]
    list_display_links = ['server']
    list_filter = ['server']
    date_hierarchy = 'updatedAt'
    search_fields = ['rootPwd.password',
                     'remark', ]
    search_help_text = ['你好，这是搜索帮助语句！']
    autocomplete_fields = ['rootPwd', 'server']
    inlines = [DbServerUserInlineAdmin]

    def _password(self, obj):
        return BaseAdmin.password(obj.rootPwd.password)

    _password.short_description = "root密码"
