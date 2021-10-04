from django.contrib import admin

from .admin import BaseAdmin
from miniProgram.models import SubscriptionAccount


@admin.register(SubscriptionAccount)
class SubscriptionAccountAdmin(admin.ModelAdmin):
    list_display = BaseAdmin.list_display + ['appId', 'appSecret']
