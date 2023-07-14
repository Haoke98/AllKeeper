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

from ..models import Weibo


@admin.register(Weibo)
class WeiboAdmin(admin.ModelAdmin):
    list_display = ["id", "avatar", "name", 'gender', 'birthday', 'zodiac', 'school', 'description', 'registeredAt',
                    'followersCount', 'friendsCount', 'statusesCount', 'location', 'ipLocation', 'isSVIP', 'userType',
                    'mbrank', 'mbtype', 'pcNew', 'sunshineCredit', 'labels']
    search_fields = ['id', 'name', 'description', 'labels']
    list_filter = ['gender', 'birthday', 'zodiac', 'school', 'location', 'ipLocation', 'isSVIP', 'userType', 'mbrank',
                   'mbtype', 'pcNew', 'registeredAt', 'sunshineCredit']
    list_per_page = 14
    inlines = []
    actions = ['collect_data', 'update', 'clear_avatar_url']

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if not change:
            obj.collect()
        else:
            pass
        return super().save_model(request, obj, form, change)

    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '120px',
            'align': 'center'
        },
        'createdAt': {
            'width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'width': '180px',
            'align': 'left'
        },
        'name': {
            'width': '200px',
            'align': 'left'
        },
        'idCardNum': {
            'width': '200px',
            'align': 'left'
        },
        'birthday': {
            'width': '110px',
            'align': 'left'
        },
        'registeredAt': {
            'width': '180px',
            'align': 'left'
        },
        'collage':{
            'width': '120px',
            'align': 'left'
        },

        'description':{
            'width': '200px',
            'align': 'left'
        },
        'WB_ID':{
            'width': '120px',
            'align': 'left'
        },
        'douyin':{
            'width': '120px',
            'align': 'left'
        },
        'license_plate_number':{
            'width': '120px',
            'align': 'left'
        },
        'labels':{
            'width': '400px',
            'align': 'left'
        },
    }

    def collect_data(self, request, queryset):
        print("采集数据中:", queryset)
        a = queryset[0].id
        b = queryset[1].id
        ab = sorted([a, b])
        print(a, b)
        print(ab)
        # max_id = Weibo.objects.aggregate(Max('id'))['id__max']
        # min_id = Weibo.objects.aggregate(Min('id'))['id__min']
        total = 0
        for id in range(ab[0], ab[1]):
            obj = Weibo(id=id)
            if obj.collect():
                obj.save()
                print(f"采集了微博账户[{obj.id}]")
                total += 1
            else:
                print(f"微博账户[{id}]不存在或者存在异常")
        print("本次总共采集了", total, "个账户数据")

    collect_data.short_description = "采集数据"

    def update(self, request, queryset):
        for qs in queryset:
            print(f"正在更新微博账户[{qs.id}]")
            qs.collect()
            qs.save()
            print(f"更新微博账户[{qs.id}]成功")

    update.short_description = "更新数据"

    def clear_avatar_url(self, request, queryset):
        for qs in queryset:
            if qs.avatar:
                fn = str(qs.avatar).split("/")[-1]
                if fn.endswith(".png"):
                    qs.collect()
                    qs.save()
                else:
                    newUri = f"/weibo_avatar/{fn}"
                    print(qs.avatar, fn, newUri)
                    qs.avatar = newUri
                    qs.save()
            else:
                qs.collect()
                qs.save()

    def formatter(self, obj, field_name, value):
        # if field_name == "avatar":
        #     if value:
        #         url = f"https://weibo.com/u/{obj.id}"
        #         return f'''<a href="{url}" target="blank"><img src="{value}" title="{obj.name}"></a>'''
        # 这里可以对value的值进行判断，比如日期格式化等
        return value
