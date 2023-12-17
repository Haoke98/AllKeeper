from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum
from simplepro.admin import LIST_DISPLAY

from .models import Debt


class ItemChangeList(ChangeList):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        self.aggregate_values = queryset.aggregate(Sum('principle'), Sum('interest'))
        return queryset


# Register your models here.
@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['sum', 'principle', 'interest', 'paid_off', 'ddl', 'whose', 'created_at']
    date_hierarchy = 'ddl'
    list_filter = ['paid_off', 'whose', 'ddl']
    ordering = ('ddl',)
    change_list_template = 'admin/Debt/change_list.html'

    def sum(self, obj):
        return obj.principle + obj.interest

    def get_changelist(self, request, **kwargs):
        return ItemChangeList

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        print(response.context_data['cl'].aggregate_values)
        aggvs = response.context_data['cl'].aggregate_values
        extra_context = extra_context or {}
        extra_context['principle__sum'] = aggvs['principle__sum']
        extra_context['interest__sum'] = aggvs['interest__sum']
        extra_context['sum'] = aggvs['interest__sum']+aggvs['principle__sum']
        return super().changelist_view(request, extra_context=extra_context)


