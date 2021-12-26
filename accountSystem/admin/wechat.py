from django.contrib import admin
from accountSystem.models import Wechat
from izBasar.admin import LIST_DISPLAY


@admin.register(Wechat)
class UniversalAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['wx_id', 'nickName', 'password', 'tel', 'group', 'remark']
    list_display_links = ['wx_id', 'nickName']
    date_hierarchy = 'updatedAt'
    search_fields = ['wx_id', 'nickName', 'remark']
    list_filter = ['tel', 'group']
    list_select_related = ['group', 'password']
    autocomplete_fields = ['tel', 'password', 'group']
    list_per_page = 8
    actions = []
