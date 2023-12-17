from simplepro.admin import BaseAdmin


class BaseServiceAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['server', 'port']
    autocomplete_fields = ['system']
    list_select_related = ['server']
