from django.contrib import admin

from accountSystem.models.email import Email
from accountSystem.models.group import Group
from accountSystem.models.password import Password
from accountSystem.models.tel import Tel
from accountSystem.models.type import Type
from izBasar.admin import LIST_DISPLAY


# TODO：把这里的所有都移植到 __init__.py中去，然后把这个admin包中的admin.py文件删除了。

# Register your admin models here.
@admin.register(Tel, Email)
class UniversalAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['content', 'remark']
    list_display_links = ['content']
    search_fields = ['content']


@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['password', ]
    search_fields = ['password']


@admin.register(Group, Type)
class GroupAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ["__str__"]
    search_fields = ['name']
    list_per_page = 14
