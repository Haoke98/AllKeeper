from django.contrib import admin

from .admin import MyModelAdmin
from miniProgram.models import SubscriptionAccount


@admin.register(SubscriptionAccount)
class SubscriptionAccountAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['appId', 'appSecret']
