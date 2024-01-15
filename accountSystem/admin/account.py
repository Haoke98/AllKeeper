from django.contrib import admin
from django.utils.safestring import mark_safe
from simplepro.admin import FieldOptions

from accountSystem.admin.base import BaseAccountAdmin
from accountSystem.forms import AccountForm
from accountSystem.models import Account, Tel, Email


@admin.register(Account)
class AccountAdmin(BaseAccountAdmin):
    list_display = ['id', 'group', 'platform', 'username', 'pwd', 'url', '_tels', '_emails', 'wechat', '_info',
                    'name'
                    ]
    date_hierarchy = 'updatedAt'
    search_fields = ['name', 'username', 'url', 'info', 'types__name', 'wechat__id', 'wechat__nickName',
                     'wechat__remark', 'platform__name', 'platform__url']
    list_filter = ['group', 'platform', 'tels', 'emails', 'types', 'wechat']
    list_select_related = ['group', 'wechat']
    autocomplete_fields = ['platform', 'tels', 'emails', 'types', 'wechat', 'group']
    list_per_page = 8
    actions = []
    form = AccountForm

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "platform":
            if value:
                return f"""<a href="{obj.platform.url}" target="_blank">{value}</a>"""
        if field_name == "url":
            if value:
                return f"""<a href="{value}" target="_blank">点击跳转</a>"""
        if field_name == "name":
            if value:
                return f'''<el-button type="info" onclick="goToDetail(this)" round>{value}</el-button>'''
        return super(AccountAdmin, self).formatter(obj, field_name, value)

    def _info(self, obj):
        if obj.info:
            tag = mark_safe(
                '''<i class="circular info icon link" data-id="%s" data-title="%s"
                ></i>''' % (
                    obj.id, obj.name))
        else:
            tag = "-"
        return tag

    def _tels(self, obj):
        items: str = ""
        tels = obj.tels.all()
        for tel in tels:
            items += self._getTelItem(tel)
        finalList = '''
                <div class="ui list">
                    %s              
                </div>
        ''' % items
        return mark_safe(finalList)

    _tels.short_description = "手机号"

    def _getTelItem(self, tel: Tel):
        item = '''
                        <div class="item">
                            <i class="phone square icon"></i>
                            <div class="content">
                              <a class="header">%s</a>
                              
                            </div>
                        </div>
                ''' % tel.content
        return mark_safe(item)

    def _emails(self, obj: Account):
        items: str = ""
        emails = obj.emails.all()
        for email in emails:
            items += self._getEmailItem(email)
        finalList = '''
                <div class="ui list">
                    %s              
                </div>
        ''' % items
        return mark_safe(finalList)

    _emails.short_description = "电子邮箱"

    def _getEmailItem(self, email: Email):
        item = '''
                        <div class="item">
                            <i class="paper plane icon"></i>
                            <div class="content">
                              <a class="header">%s</a>

                            </div>
                        </div>
                ''' % email.username
        return mark_safe(item)

    fields_options = {
        'id': FieldOptions.UUID,
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'platform': {
            'min_width': '160px',
            'align': 'left',
            "resizeable": True,
            "show_overflow_tooltip": True
        },
        'username': FieldOptions.USER_NAME,
        'pwd': FieldOptions.PASSWORD,
        'url': {
            'width': '130px',
            'align': 'center'
        },
        '_tels': {
            'min_width': '120px',
            'align': 'left',
            "resizeable": True,
            "show_overflow_tooltip": True
        },
        '_emails': {
            'min_width': '140px',
            'align': 'left',
            "resizeable": True,
            "show_overflow_tooltip": True
        },
        'wechat': {
            'min_width': '120px',
            'align': 'left',
            "resizeable": True,
            "show_overflow_tooltip": True
        },

        'info': {
            'width': '180px',
            'align': 'left'
        },
        'group': {
            'min_width': '140px',
            'align': 'left',
            "resizeable": True,
            "show_overflow_tooltip": True
        },
        'name': {
            'width': '200px',
            'align': 'center'
        },
        'createdUserRecordName': {
            'width': '300px',
            'align': 'left'
        },
        'modifiedUserRecordName': {
            'width': '300px',
            'align': 'left'
        },
        'createdDeviceID': {
            'width': '400px',
            'align': 'left'
        },
        'modifiedDeviceID': {
            'width': '400px',
            'align': 'left'
        },
        'locationEnc': {
            'width': '1000px',
            'align': 'left'
        },
    }
