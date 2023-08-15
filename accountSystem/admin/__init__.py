from django.contrib import admin

# Register your admin models here.
from accountSystem.models.type import Type
from izBasar.admin import LIST_DISPLAY
from .account import AccountAdmin, Account
from .breath import BreathInfoAdmin
from .bt import BtAdmin
from .bt import BtAdmin
from .dbService import DbServiceAdmin
from .dbService import DbServiceAdmin
from .dbServiceUser import DbServiceUserAdmin
from .dbServiceUser import DbServiceUserAdmin
from .email import EmailAdmin
from .es import ElasticSearchAdmin
from .human import HumanAdmin
from .icloud import IMediaAdmin
from .market_subject import MarketSubjectAdmin
from .scripts import ScriptAdmin
from .server import ServerAdmin
from .server import ServerAdmin
from .serverUser import ServerUserAdmin
from .serverUser import ServerUserAdmin
from .tel import TelAdmin
from .tel import TelAdmin
from .trade import CapitalAccountAdmin, TransactionAdmin
from .wechat import WechatAdmin
from .weibo import WeiboAdmin


@admin.register(Type)
class GroupAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ["__str__", '_count']
    search_fields = ['name']
    list_per_page = 14

    def _count(self, obj):
        return Account.objects.filter(types=obj.id).count()
