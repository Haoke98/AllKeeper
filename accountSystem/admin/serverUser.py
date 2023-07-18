from django.contrib import admin

from izBasar.admin import LIST_DISPLAY, BaseAdmin
from ..forms import ServerUserForm
from ..models import ServerUser


@admin.register(ServerUser)
class ServerUserAdmin(BaseAdmin):
    list_display = LIST_DISPLAY + ['_username', '_password', 'hasRootPriority', '_ip', 'owner']
    autocomplete_fields = ['server', 'owner']
    list_filter = ['hasRootPriority', 'server', 'owner']
    list_select_related = autocomplete_fields
    form = ServerUserForm

    def _username(self, obj):
        return BaseAdmin.username(obj.username)

    def _password(self, obj):
        return BaseAdmin.password(obj.pwd)

    _password.short_description = "密码"

    def _ip(self, obj):
        return BaseAdmin.username(obj.server.ip)

    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '40px',
            'align': 'center'
        },
        'createdAt': {
            'width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'width': '180px',
            'align': 'left'
        },
        '_ip': {
            'width': '140px',
            'align': 'center'
        },
        'ssh': {
            'width': '120px',
            'align': 'center'
        },
        'hoster': {
            'width': '320px',
            'align': 'left'
        },
        'group': {
            'width': '220px',
            'align': 'left'
        },
        '_password': {
            'width': '80px',
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
