from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.
@admin.register(TTel, EEmail)
class UniversalAdmin(admin.ModelAdmin):
    list_display = ['id', 'content']
    list_display_links = ['content']


@admin.register(PPassword)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ['password', ]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['__str__', '_username', '_password', '_url', 'email', 'tel', 'Introduce']

    def _url(self, obj):
        if obj.url:
            tag = mark_safe('<a href="%s" target="blank">%s</a>' % (obj.url, obj.url))
        else:
            tag = "-"
        return tag

    _url.allow_tags = True

    def _password(self, obj):
        tag = mark_safe('''<div class="username-password-div" ><label>********</label><img src="%s" class="copyImg" onclick="copyStr('%s')"><div>''' % (
            str(
                "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fbpic.588ku.com%2Felement_origin_min_pic%2F00%2F20%2F25%2F2356cd187bdb078.jpg&refer=http%3A%2F%2Fbpic.588ku.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1618941661&t=55d40f81ef710d6eb4995f88aaefc9c2"),
            obj.password.password))
        return tag

    _password.allow_tags = True

    def _username(self, obj):
        tag = mark_safe('''<div class="username-password-div" ><label>%s</label><img src="%s" class="copyImg" onclick="copyStr('%s')"></div>''' % (
            obj.username, str(
                "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fbpic.588ku.com%2Felement_origin_min_pic%2F00%2F20%2F25%2F2356cd187bdb078.jpg&refer=http%3A%2F%2Fbpic.588ku.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1618941661&t=55d40f81ef710d6eb4995f88aaefc9c2"),
            obj.username))
        return tag

    _username.allow_tags = True
    # list_display = ['__str__', 'username',  ,'url',  'Introduce']
