from django.contrib import admin

from izBasar.admin import LIST_DISPLAY, BaseAdmin
from ..forms import DbServiceUserForm, DbServiceUserFormBase
from ..models import DbServiceUser


@admin.register(DbServiceUser)
class DbServiceUserAdmin(BaseAdmin):
    list_display = LIST_DISPLAY + ['_username', '_password', 'hasRootPriority', 'server', 'owner']
    autocomplete_fields = ['server', 'owner']
    list_filter = ['hasRootPriority', 'server', 'owner']
    list_select_related = autocomplete_fields
    raw_id_fields = ('owner', 'server')
    form = DbServiceUserForm

    def _username(self, obj):
        return BaseAdmin.username(obj.username)

    def _password(self, obj):
        return BaseAdmin.password(obj.password)

    _password.short_description = "密码"


class DbServiceUserInlineAdmin(admin.TabularInline):
    model = DbServiceUser
    autocomplete_fields = ['server', 'owner']
    exclude = ('password',)
    min_num = 0
    extra = 0
    form = DbServiceUserFormBase
