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
    list_display = LIST_DISPLAY + ["name", 'icon', 'url', '_count']
    search_fields = ['name', 'url']
    list_per_page = 14

    def _count(self, obj):
        return Account.objects.filter(types=obj.id).count()

    _count.short_description = "关联账号的数量"

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "url":
            if value:
                return f"""<a href="{value}" target="_blank">点击跳转</a>"""
        return value

    fields_options = {
        'id': {
            'fixed': 'left',
            'min_width': '80px',
            'align': 'center'
        },
        'createdAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'deletedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'name': {
            'min_width': '300px',
            'align': 'center'
        },
        'icon': {
            'min_width': '160px',
            'align': 'center'
        },
        'url': {
            'min_width': '180px',
            'align': 'center'
        },
        '_count': {
            'min_width': '120px',
            'align': 'center'
        }
    }
