from django.contrib import admin

from .models import *


# Register your models here.


@admin.register(settings)
class settingsAdmin(admin.ModelAdmin):
    list_display = ['app_name', 'app_id', 'app_secret']


@admin.register(film)
class kinoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'cover', ]


@admin.register(video)
class episodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'cover', 'url', 'belongTo']
