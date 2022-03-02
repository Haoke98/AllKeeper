from django.contrib import admin

from accountSystem.models.email import Email
from accountSystem.models.group import Group
from accountSystem.models.password import Password
from accountSystem.models.type import Type
from izBasar.admin import LIST_DISPLAY
from .account import AccountAdmin, Account
from .bt import BtAdmin
from .bt import BtAdmin
from .dbService import DbServiceAdmin
from .dbService import DbServiceAdmin
from .dbServiceUser import DbServiceUserAdmin
from .dbServiceUser import DbServiceUserAdmin
from .es import ElasticSearchAdmin
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
    list_display = LIST_DISPLAY + ["__str__", '_count']
    search_fields = ['name']
    list_per_page = 14

    def _count(self, obj):
        return Account.objects.filter(types=obj.id).count()
