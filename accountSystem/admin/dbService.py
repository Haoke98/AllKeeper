from django.contrib import admin

from izBasar.admin import LIST_DISPLAY, BaseAdmin
from .dbServiceUser import DbServiceUserInlineAdmin
from ..forms import DbServiceForm
from ..models import DbService


@admin.register(DbService)
class DbServiceAdmin(BaseAdmin):
    form = DbServiceForm
    list_display = LIST_DISPLAY + ['server',
                                   'port', '_password', 'remark', ]
    list_display_links = ['server', 'port']
    list_filter = ['server', 'port']
    date_hierarchy = 'updatedAt'
    search_fields = ['rootPwd.password',
                     'remark', ]
    search_help_text = ['你好，这是搜索帮助语句！']
    autocomplete_fields = ['server']
    inlines = [DbServiceUserInlineAdmin]

    def _password(self, obj):
        return BaseAdmin.password(obj.pwd)

    _password.short_description = "root密码"
