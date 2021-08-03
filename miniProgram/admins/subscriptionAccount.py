from django.contrib import admin

from miniProgram.admins.admin import MyModelAdmin
from miniProgram.models.subscriptionAccount import SubscriptionAccount


@admin.register(SubscriptionAccount)
class SubscriptionAccountAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['appId', 'appSecret']
