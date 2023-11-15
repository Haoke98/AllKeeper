from django.contrib import admin

from izBasar.admin import LIST_DISPLAY, BaseAdmin
from ..forms import DbServiceUserForm, DbServiceUserFormBase
from ..models import DbServiceUser


@admin.register(DbServiceUser)
class DbServiceUserAdmin(BaseAdmin):
    list_display = LIST_DISPLAY + ['username', 'password', 'hasRootPriority', 'service', 'owner']
    autocomplete_fields = ['service']
    list_filter = ['hasRootPriority', 'service', 'owner']
    list_select_related = autocomplete_fields
    raw_id_fields = ('service',)
    form = DbServiceUserForm

    def formatter(self, obj, field_name, value):
        if field_name == 'username':
            if value:
                return BaseAdmin.password(obj.username)
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
        'server': {
            'min_width': '320px',
            'align': 'center'
        },
        'owner': {
            'min_width': '178px',
            'align': 'center'
        }
    }


class DbServiceUserInlineAdmin(admin.TabularInline):
    model = DbServiceUser
    autocomplete_fields = ['service']
    exclude = ('password',)
    min_num = 0
    extra = 0
    form = DbServiceUserFormBase
