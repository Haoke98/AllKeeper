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
from django.db.models import Max, Min
def collect_data(modeladmin, request, queryset):
    print("采集数据中:",queryset)
    a = queryset[0].id
    b = queryset[1].id
    ab = sorted([a,b])
    print(a,b)
    print(ab)
    # max_id = Weibo.objects.aggregate(Max('id'))['id__max']
    # min_id = Weibo.objects.aggregate(Min('id'))['id__min']
    total = 0
    for id in range(ab[0],ab[1]):
        obj = Weibo(id=id)
        if obj.collect():
            obj.save()
            print(f"采集了微博账户[{obj.id}]")
            total +=1
        else:
            print(f"微博账户[{id}]不存在或者存在异常")
    print("本次总共采集了",total,"个账户数据")
collect_data.short_description = "采集数据"

def update(modeladmin, request, queryset):
    for qs in queryset:
        print(f"正在更新微博账户[{qs.id}]")
        qs.collect()
        print(f"更新微博账户[{qs.id}]成功")
update.short_description= "更新数据"
@admin.register(Weibo)
class WeiboAdmin(admin.ModelAdmin):
    list_display = ["id","_avatar","name",  'gender', 'birthday', 'zodiac', 'school','description' ,'registeredAt','followersCount','friendsCount','statusesCount','location','ipLocation','isSVIP','userType','mbrank','mbtype','pcNew','sunshineCredit','labels']
    search_fields = ['id','name','description','labels']
    list_filter = ['gender', 'birthday', 'zodiac','school','location','ipLocation','isSVIP','userType','mbrank','mbtype','pcNew','registeredAt','sunshineCredit']
    list_per_page = 14
    inlines = []
    actions = [collect_data,update]
    
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
            pass
        else:
            pass
        return super().save_model(request, obj, form, change)

    # 显示在列表顶部的一些自定义html，可以是vue组件，会被vue渲染
    top_html = ' <el-alert title="这是顶部的" type="success"></el-alert>'
    # 也可以是方法的形式来返回html

    def get_top_html(self, request):
        return self.top_html
    
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px',
            'align': 'center'
        },
        'create_time': {
            'fixed': 'right',
            'width': '200px',
            'align': 'left'
        }
    }