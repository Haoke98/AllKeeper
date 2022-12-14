from django.contrib import admin

from accountSystem.models.email import Email
from izBasar.admin import LIST_DISPLAY


# Register your admin models here.
@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['username', 'remark', 'pwd', 'group']
    list_display_links = ['username']
    list_filter = ['group']
    list_select_related = ['group']
    search_fields = ['username', 'remark', 'group__name']
