# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/6/13
@Software: PyCharm
@disc:
======================================="""
from typing import Any
from django.contrib import admin
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from izBasar.admin import LIST_DISPLAY
from lib import imageHelper,weiboHelper
from ..models import Weibo

@admin.register(Weibo)
class WeiboAdmin(admin.ModelAdmin):
    list_display = ["id","_avatar","name",  'gender', 'birthday', 'zodiac', 'school','description' ,'followersCount','friendsCount','statusesCount','location','isSVIP','userType']
    search_fields = ['id','name','description']
    list_filter = ['gender', 'birthday', 'zodiac','school','location','isSVIP','userType']
    list_per_page = 14
    inlines = []

    
    def _avatar(self, obj):
        if obj.avatar:
            url = f"https://weibo.com/u/{obj.id}"
            profile_image_base64 = imageHelper.image_to_base64(obj.avatar)
            return mark_safe(f'''
            <a href="{url}" target="blank"><img src="data:image/jpeg;base64,{profile_image_base64}" title="{obj.name}"></a>
            ''')
        else:
            return None

    _avatar.short_description = "微博头像"

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if not change:
            print("正在新建微博账户:",obj.id)
            infoResp = weiboHelper.info(obj.id)
            detailResp = weiboHelper.detail(obj.id)
            userInfo = infoResp['user']
            print(userInfo)
            obj.name = userInfo['screen_name']
            obj.avatar = userInfo['profile_image_url']
            obj.description = userInfo['description']
            obj.location = userInfo['location']
            obj.gender = userInfo['gender']
            obj.followersCount = userInfo['followers_count']
            obj.friendsCount = userInfo['friends_count']
            obj.statusesCount = userInfo['statuses_count']
            if userInfo['svip']==1:
                obj.isSVIP = True
            obj.userType = userInfo['user_type']
        else:
            print("Form: ",form)
        return super().save_model(request, obj, form, change)
