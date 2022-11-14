from django.contrib import admin
from django.utils.safestring import mark_safe

from accountSystem.forms import AccountForm
from accountSystem.models import Account, Tel, Email, Type
from izBasar.admin import BaseAdmin


@admin.register(Account)
class AccountAdmin(BaseAdmin):
    list_display = ['id', 'platform', '_username', '_password', '_url', '_tels', '_emails', 'wechat', '_info',
                    '_name'
                    ]
    list_display_links = ['id', 'platform']
    date_hierarchy = 'updatedAt'
    search_fields = ['name', 'username', 'url', 'info', 'types__name', 'wechat__id', 'wechat__nickName',
                     'wechat__remark', 'platform__name', 'platform__url']
    list_filter = ['group', 'platform', 'tels', 'emails', 'types', 'wechat']
    list_select_related = ['group', 'wechat']
    autocomplete_fields = ['platform', 'tels', 'emails', 'types', 'wechat', 'group']
    list_per_page = 8
    actions = []
    form = AccountForm

    def _url(self, obj):
        if obj.platform is not None:
            return BaseAdmin.shwoUrl(obj.platform.url)
            # TODO:判断灵活的数据url，本应该是type的URL。
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
        return BaseAdmin.password(obj.pwd)

    _password.allow_tags = True

    def _username(self, obj):
        return BaseAdmin.username(obj.username)

    _username.allow_tags = True

    def _name(self, obj):
        tag = mark_safe(
            '''<a class="ui teal tag label" style="width:10em;white-space:nowrap;" onclick="goToDetail(this)">%s</a>''' % obj.name)
        return tag

    _name.allow_tags = True

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
        ]
