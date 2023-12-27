from django.contrib import admin
from simplepro.admin import LIST_DISPLAY, FieldOptions, BaseAdmin

from .base import BaseAccountAdmin
from ..models import Email


# Register your admin models here.
@admin.register(Email)
class EmailAdmin(BaseAccountAdmin):
    list_display = LIST_DISPLAY + ['username', 'pwd', 'group', 'remark']
    list_display_links = ['username']
    list_filter = ['group']
    list_select_related = ['group']
    search_fields = ['username', 'remark', 'group__name']

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "name":
            if value:
                return f'''<el-button type="info" onclick="goToDetail(this)" round>{value}</el-button>'''
        return super(EmailAdmin, self).formatter(obj, field_name, value)

    fields_options = {
        'id': FieldOptions.UUID,
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'username': FieldOptions.EMAIL,
        'pwd': FieldOptions.PASSWORD,
        'remark': {
            'min_width': '240px',
            'align': 'left'
        },
        'group': {
            'min_width': '180px',
            'align': 'left'
        }
    }
