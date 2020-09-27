from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(User)
class userAdmin(admin.ModelAdmin):
    list_display = ['openid', 'vip_expiredTime', 'last_changed_time', 'firstTimeLogin']


@admin.register(subcribtions)
class subcribtionsAdmin(admin.ModelAdmin):
    list_display = ['name', 'app_id', 'app_secret']


@admin.register(settings)
class settingsAdmin(admin.ModelAdmin):
    list_display = ['app_name', 'enableVIP_mode', 'app_id', 'app_secret', 'subcribtion']


@admin.register(film)
class kinoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'cover', ]


@admin.register(video)
class episodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'cover', 'url', 'belongTo']
