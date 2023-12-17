from django.contrib import admin
from simplepro.admin import BaseAdmin, LIST_DISPLAY

from ..models import DbServiceUser


@admin.register(DbServiceUser)
class DbServiceUserAdmin(BaseAdmin):
    list_display = LIST_DISPLAY + ['username', 'password', 'hasRootPriority', 'service', 'owner']
    autocomplete_fields = ['service']
    list_filter = ['hasRootPriority', 'service', 'owner']
    list_select_related = autocomplete_fields

    def formatter(self, obj, field_name, value):
        if field_name == 'username':
            if value:
                return BaseAdmin.username(obj.username)
        if field_name == 'password':
            if value:
                return BaseAdmin.password(obj.password)
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
        'username': {
            'min_width': '200px',
            'align': 'left'
        },
        'password': {
            'min_width': '180px',
            'align': 'center'
        },
        'hasRootPriority': {
            'min_width': '140px',
            'align': 'center'
        },
        'service': {
            'min_width': '320px',
            'align': 'left'
        },
        'owner': {
            'min_width': '240px',
            'align': 'left'
        }
    }


class DbServiceUserInlineAdmin(admin.TabularInline):
    model = DbServiceUser
    autocomplete_fields = ['service']
    exclude = ('password',)
    min_num = 0
    extra = 0
