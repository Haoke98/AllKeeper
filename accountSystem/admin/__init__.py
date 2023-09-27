from urllib.parse import urlparse

from django.contrib import admin

# Register your admin models here.
from accountSystem.models.type import Platform
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


@admin.register(Platform)
class GroupAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ["name", 'icon', 'url', 'hostname', 'path', '_count']
    search_fields = ['name', 'url']
    list_per_page = 14

    def _count(self, obj):
        return Account.objects.filter(types=obj.id).count()

    _count.short_description = "关联账号的数量"

    # TODO: 把这个改成模型属性
    def hostname(self, obj):
        if obj.url:
            res = urlparse(obj.url)
            return res.hostname

    # TODO: 把这个动态解析改成模型属性
    def path(self, obj):
        if obj.url:
            res = urlparse(obj.url)
            return res.path

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "url":
            if value:
                return f"""<a href="{value}" target="_blank">点击跳转</a>"""
        if field_name == "icon":
            if value:
                return '''<el-image style="width: 100px; height: 100px" src="{}" :preview-src-list="['{}']" lazy></el-image>'''.format(
                    value, value)
            else:
                if obj.url:
                    res = urlparse(obj.url)
                    icon_url = f"{res.scheme}://{res.hostname}/favicon.ico"
                    return '''<el-image style="width: 100px; height: 100px" src="{}" :preview-src-list="['{}']" lazy></el-image>'''.format(
                        icon_url, icon_url)
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
        },
        'hostname': {
            'min_width': '200px',
            'align': 'left'
        },
        'path': {
            'min_width': '220px',
            'align': 'left'
        }
    }
