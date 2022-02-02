from django.contrib import admin

from accountSystem.models.email import Email
from accountSystem.models.group import Group
from accountSystem.models.password import Password
from accountSystem.models.type import Type
from izBasar.admin import LIST_DISPLAY
from .account import AccountAdmin
from .account import AccountAdmin
from .bt import BtAdmin
from .bt import BtAdmin
from .dbServer import DbServerAdmin
from .dbServer import DbServerAdmin
from .dbServerUser import DbServerUserAdmin
from .dbServerUser import DbServerUserAdmin
from .server import ServerAdmin
from .server import ServerAdmin
from .serverUser import ServerUserAdmin
from .serverUser import ServerUserAdmin
from .tel import TelAdmin
from .tel import TelAdmin
from .wechat import WechatAdmin

# Register your admin models here.
@admin.register(Email)
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
