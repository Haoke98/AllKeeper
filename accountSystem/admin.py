from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ['password', ]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'username', 'password', 'url', 'email', 'Introduce']