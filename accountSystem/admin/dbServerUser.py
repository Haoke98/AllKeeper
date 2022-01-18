from django.contrib import admin
from izBasar.admin import LIST_DISPLAY, BaseAdmin
from ..models import DbServerUser


@admin.register(DbServerUser)
class DbServerUserAdmin(BaseAdmin):
    list_display = LIST_DISPLAY + ['username', '_password', 'hasRootPriority', 'server', 'owner']
    autocomplete_fields = ['password', 'server', 'owner']
    list_filter = ['hasRootPriority', 'server', 'owner']
    list_select_related = autocomplete_fields

    def _password(self, obj):
        return BaseAdmin.password(obj.password.password)

    _password.short_description = "密码"


class DbServerUserInlineAdmin(admin.TabularInline):
    model = DbServerUser
    autocomplete_fields = ['password', 'server', 'owner']
    min_num = 0
    extra = 0
