from django.contrib import admin

from izBasar.admin import LIST_DISPLAY
from .models import Debt


# Register your models here.
@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['sum', 'principle', 'interest', 'paid_off', 'ddl', 'whose', 'created_at']
    date_hierarchy = 'ddl'
    list_filter = ['paid_off', 'whose', 'created_at']

    def sum(self, obj):
        return obj.principle + obj.interest
