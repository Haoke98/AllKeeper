from django.contrib import admin
from django.utils.safestring import mark_safe

from accountSystem.forms import AccountForm
from accountSystem.models import Account, Tel, Email, Type
from izBasar.admin import BaseAdmin


@admin.register(Account)
class AccountAdmin(BaseAdmin):
    list_display = ['id', 'platform', 'username', 'pwd', 'url', '_tels', '_emails', 'wechat', '_info',
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
        if field_name == "username":
            if value:
                return BaseAdmin.username(obj.username)
        if field_name == 'pwd':
            if value:
                return BaseAdmin.password(obj.pwd)
        if field_name == "platform":
            if value:
                return f"""<a href="{obj.platform.url}" target="_blank">{value}</a>"""
        if field_name == "url":
            if value:
                return f"""<a href="{value}" target="_blank">点击跳转</a>"""
        if field_name == "name":
            if value:
                return f'''<el-button type="info" onclick="goToDetail(this)" round>{value}</el-button>'''
        return value

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

    def _types(self, obj: Account):
        items: str = ""
        types = obj.types.all()
        for item in types:
            items += self._getTypeItem(item)
        result = '''
                        <div class="ui list">
                            %s              
                        </div>
                ''' % items
        return mark_safe(result)

    def _getTypeItem(self, email: Type):
        item = '''
                        <div class="item">
                            <i class="paper plane icon"></i>
                            <div class="content">
                              <a class="header">%s</a>

                            </div>
                        </div>
                ''' % email.name
        return mark_safe(item)

    fields_options = {
        'id': {
            # 'fixed': 'left',
            'width': '80px',
            'align': 'center'
        },
        'createdAt': {
            'width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'width': '180px',
            'align': 'left'
        },
        'platform': {
            'width': '200px',
            'align': 'left'
        },
        'username': {
            'width': '260px',
            'align': 'left'
        },
        'pwd': {
            'width': '200px',
            'align': 'center'
        },
        'url': {
            'width': '130px',
            'align': 'center'
        },
        '_tels': {
            'width': '180px',
            'align': 'left'
        },
        '_emails': {
            'width': '200px',
            'align': 'left'
        },
        'wechat': {
            'width': '120px',
            'align': 'left'
        },

        'info': {
            'width': '180px',
            'align': 'left'
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
