from django.contrib import admin
from django.utils.safestring import mark_safe

from accountSystem.models import Account, Tel, Email, Type
from izBasar.admin import LIST_DISPLAY,BaseAdmin


@admin.register(Account)
class AccountAdmin(BaseAdmin):
    list_display = LIST_DISPLAY + ['_name', '_username', '_password', '_url', '_tels', '_emails', 'wechat', '_info',
                                   '_types']
    list_display_links = ['id', '_name']
    date_hierarchy = 'updatedAt'
    search_fields = ['name', 'username', 'url', 'info', 'types__name', 'wechat__wx_id', 'wechat__nickName',
                     'wechat__remark']
    list_filter = ['group', 'tels', 'emails', 'types', 'wechat']
    list_select_related = ['group', 'password', 'wechat']
    autocomplete_fields = ['tels', 'emails', 'password', 'group', 'types', 'wechat']
    list_per_page = 8
    actions = []

    def _url(self, obj):
        return BaseAdmin.shwoUrl(obj.url)

    _url.allow_tags = True

    def _info(self, obj):
        if obj.info:
            tag = mark_safe(
                '''<i class="circular info icon link" data-id="%s" data-title="%s"
                ></i>''' % (
                    obj.id, obj.name))
        else:
            tag = "-"
        return tag

    _url.allow_tags = True

    def _password(self, obj):
        return BaseAdmin.password(obj.password.password)

    _password.allow_tags = True

    def _username(self, obj):
        return BaseAdmin.username(obj.username)

    _username.allow_tags = True

    def _name(self, obj):
        tag = mark_safe(
            '''<a class="ui teal tag label" style="width:20em;" onclick="goToDetail(this)">%s</a>''' % obj.name)
        return tag

    _name.allow_tags = True

    def _tels(self, obj):
        items: str = ""
        tels = obj.tels.all()
        print(obj.id, obj.name, tels)
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
        print(obj.id, obj.name, emails)
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
                ''' % email.content
        return mark_safe(item)

    def _types(self, obj: Account):
        items: str = ""
        types = obj.types.all()
        print(obj.id, obj.name, types)
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

    def actionTelAndEmailMigration(self, request, queryset):
        for obj in queryset:
            obj.types.add(obj.type)
            obj.save()

    actionTelAndEmailMigration.short_description = '数据迁移升级操作'

    class Media:

        def __init__(self):
            pass

        css = {
        }
        js = [
            'kindeditor4.1.11/kindeditor-all.js',
            'kindeditor4.1.11/lang/zh-CN.js',

            'js/config-account-admin.js',
        ]
    