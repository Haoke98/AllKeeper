from django.contrib import admin
from izBasar.admin import LIST_DISPLAY
from ..models import Tel


@admin.register(Tel)
class TelAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['content', 'remark', 'owner']
    list_display_links = ['content']
    list_filter = ['owner']
    autocomplete_fields = ['owner']
    list_select_related = ['owner']
    search_fields = ['content']
