from django.contrib import admin
from simplepro.admin import LIST_DISPLAY

from utils.phoneNumHelper import get_carrier
from ..models import Tel


@admin.register(Tel)
class TelAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['content', 'remark', 'owner', '_carrier']
    list_display_links = ['content']
    list_filter = ['owner']
    autocomplete_fields = ['owner']
    list_select_related = ['owner']
    search_fields = ['content']

    def _carrier(self, obj):
        return get_carrier(obj.content)

    _carrier.short_description = "运营商"
