from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(TTel, EEmail)
class UniversalAdmin(admin.ModelAdmin):
    list_display = ['id', 'content']
    list_display_links = ['content']


@admin.register(PPassword)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ['password', ]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'username', 'password', 'url', 'email', 'tel', 'Introduce']
    # list_display = ['__str__', 'username',  ,'url',  'Introduce']
