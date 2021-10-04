from django.contrib import admin
from django.utils.safestring import mark_safe

from izBasar.admin import LIST_DISPLAY, showUrl
from .models.account import Account
from .models.accountType import AccountType
from .models.models import TTel, EEmail, PPassword, Group


# Register your models here.


@admin.register(TTel, EEmail)
class UniversalAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['id', 'content', 'remark']
    list_display_links = ['content']


@admin.register(PPassword)
class PasswordAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['password', ]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ['name', '_username', '_password', '_url', 'email', 'tel', '_info', 'type']
    list_display_links = ['name']
    date_hierarchy = 'updatedAt'
    search_fields = ['name', 'username', 'url', 'Introduce']
    list_filter = ['group', 'type', 'tel', 'email']
    list_select_related = list_filter + ['password']

    def _url(self, obj):
        return showUrl(obj.url)

    _url.allow_tags = True

    def _info(self, obj):
        if obj.Introduce:
            tag = mark_safe(
                '''<button type="button" class="button" title="%s"  onclick="copyStr('%s')" >info</button>''' % (
                    obj.Introduce, obj.Introduce))
        else:
            tag = "-"
        return tag

    _url.allow_tags = True

    def _password(self, obj):
        tag = mark_safe(
            '''<button type="button" class="button" title="%s" onclick="copyWithElement(this,'%s')" >********</button>''' % (
                obj.password.password, obj.password.password))
        return tag

    _password.allow_tags = True

    def _username(self, obj):
        tag = mark_safe(
            '''<button type="button" class="button" title="点击复制用户名" onclick="copyStr('%s')" >%s</button>''' % (
                obj.username, obj.username))
        return tag

    _username.allow_tags = True
    # list_display = ['__str__', 'username',  ,'url',  'Introduce']

    class Media:

        def __init__(self):
            pass

        js = [
            'kindeditor4.1.11/kindeditor-all.js',
            'kindeditor4.1.11/lang/zh-CN.js',
            'js/config-account-admin.js',
            'js/jquery-3.6.0.min.js',
            'js/clipboardUtil.js',
            'bootstrap-3.4.1-dist/js/bootstrap.js'
        ]

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ["__str__", "__name__"]


@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY + ["__str__", "__name__"]
