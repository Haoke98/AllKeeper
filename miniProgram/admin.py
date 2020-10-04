from django.contrib import admin

from .models import *


# Register your models here.

class MyModelAdmin(admin.ModelAdmin):
    list_display = list(admin.ModelAdmin.list_display) + ['last_changed_time']


@admin.register(User)
class userAdmin(MyModelAdmin):
    list_display = MyModelAdmin.list_display + ['last_login_time', 'vip_expiredTime', 'firstTimeLogin']


@admin.register(subcribtions)
class subcribtionsAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['app_id', 'app_secret']


@admin.register(settings)
class settingsAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['enableVIP_mode', 'app_id', 'app_secret', 'subcribtion', 'VIPprice']
    list_display_links = ['__str__', 'subcribtion']


@admin.register(film)
class kinoAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['id', 'cover', ]


@admin.register(video)
class videoAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['episode_num', 'belongTo', 'id', 'cover', 'url', ]
    list_display_links = list(admin.ModelAdmin.list_display_links) + ['belongTo', '__str__']
