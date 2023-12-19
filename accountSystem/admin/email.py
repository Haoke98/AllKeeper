from django.contrib import admin
from simplepro.admin import LIST_DISPLAY, FieldOptions, BaseAdmin

from accountSystem.models.email import Email


# Register your admin models here.
@admin.register(Email)
class EmailAdmin(BaseAdmin):
    list_display = LIST_DISPLAY + ['username', 'pwd', 'group', 'remark']
    list_display_links = ['username']
    list_filter = ['group']
    list_select_related = ['group']
    search_fields = ['username', 'remark', 'group__name']

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
