from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.

class MyModelAdmin(admin.ModelAdmin):
    list_display = list(admin.ModelAdmin.list_display) + ['last_changed_time']


@admin.register(Article)
class ArticleAdmin(MyModelAdmin):
    list_display = MyModelAdmin.list_display + ['description', 'cover_url', 'url']


@admin.register(RedirectUrlRelation)
class UrlRedirectorAdmin(MyModelAdmin):
    list_display = MyModelAdmin.list_display + ['id', '_url', 'returnValue', '_redirectUrl']

    def _redirectUrl(self, obj):
        x = mark_safe('<a href="%s">%s</a>' % (obj.redirectUrl, obj.redirectUrl))
        return x

    def _url(self, obj):
        x = mark_safe('<a href="/miniProgram/UrlRedirector%d">/miniProgram/UrlRedirector%d</a>' % (obj.id, obj.id))
        return x

    _redirectUrl.allow_tags = True


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
                                                ]
    list_display_links = ['__str__', 'subcribtion']


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['id', '_cover', '_cover1']

    def _cover(self, obj):
        try:
            if obj.cover == None:
                img = ''
            else:
                img = mark_safe('<img src="%s" width="50px" height="50px"/>' % (obj.cover,))
        except Exception as e:
            img = ''
        return img

    def _cover1(self, obj):
        return obj.cover1.show()


@admin.register(Video)
class videoAdmin(admin.ModelAdmin):
    list_display = MyModelAdmin.list_display + ['episode_num', 'belongTo', 'id', '_cover', '_cover1', 'url', ]
    list_display_links = list(admin.ModelAdmin.list_display_links) + ['belongTo', '__str__']

    def _cover(self, obj):
        try:
            if obj.cover == None:
                img = ''
            else:
                img = mark_safe('<img src="%s" width="50px" height="50px"/>' % (obj.cover,))
        except Exception as e:
            img = ''
        return img

    def _cover1(self, obj):
        if obj.cover1 == None:
            return ''
        else:
            return obj.cover1.show()

    def save_model(self, request, obj, form, change):
        print("user clicked the save button just now for this video:%s change:%s" % (obj.name, change))
        # if change:
        obj.save()


@admin.register(Image)
class ImageAdmin(MyModelAdmin):
    list_display = MyModelAdmin.list_display + ['show', 'id', 'media_id', 'content']

    def show(self, obj):
        return obj.show()
