from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.

class MyModelAdmin(admin.ModelAdmin):
    list_display = list(admin.ModelAdmin.list_display) + ['last_changed_time']


@admin.register(User)
class userAdmin(MyModelAdmin):
    list_display = MyModelAdmin.list_display + ['last_login_time', 'vip_expiredTime', 'avatar', 'nickName', '_gender',
                                                'language', 'city', 'province', 'country', 'firstTimeLogin']

    def avatar(self, obj):
        try:
            if obj.avatarUrl == None:
                img = ''
            else:
                img = mark_safe('<img src="%s" width="50px" />' % (obj.avatarUrl,))
        except Exception as e:
            img = ''
        return img

    def _gender(self, obj):
        if obj.gender == 0:
            return "女"
        elif obj.gender == 1:
            return "男"
        else:
            return "-"

    avatar.allow_tags = True


@admin.register(subcribtions)
class subcribtionsAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['app_id', 'app_secret']


@admin.register(settings)
class settingsAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['enableVIP_mode', 'VIPprice', 'app_id', 'app_secret', 'subcribtion',
                                                'banner', 'dialogBackground']
    list_display_links = ['__str__', 'subcribtion']


@admin.register(film)
class kinoAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['id', 'cover', ]


@admin.register(video)
class videoAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['episode_num', 'belongTo', 'id', 'cover', 'url', ]
    list_display_links = list(admin.ModelAdmin.list_display_links) + ['belongTo', '__str__']
