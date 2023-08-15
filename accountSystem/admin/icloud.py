# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/8/16
@Software: PyCharm
@disc:
======================================="""
import json
import os.path
import threading

from django.contrib import admin
from simplepro.decorators import button

from izBasar.secret import ICLOUD_USERNAME, ICLOUD_PASSWORD
from lib import icloud, human_readable_bytes
from ..models import IMedia


def collect_all_medias():
    iService = icloud.IcloudService(ICLOUD_USERNAME, ICLOUD_PASSWORD, True)
    all_photos = iService.photos.all
    total = len(all_photos)
    for i, p in enumerate(all_photos):
        fn, ext = os.path.splitext(p.filename)
        obj = IMedia(id=p.id, filename=p.filename, ext=str(ext).upper(), size=p.size, dimensionX=p.dimensions[0],
                     dimensionY=p.dimensions[1], asset_date=p.asset_date, added_date=p.added_date,
                     versions=json.dumps(p.versions, indent=4, ensure_ascii=False))
        obj.save()
        print(f"{i / total * 100:.2f}%({i}/{total})", p.id)
        if p.created != p.asset_date:
            raise Exception("异常数据")
        # messages.add_message(request, messages.ERROR, '操作成功123123123123')


@admin.register(IMedia)
class IMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename', 'ext', 'size', 'dimensionX', 'dimensionY', 'asset_date', 'added_date',
                    'createdAt', 'updatedAt']
    list_filter = ['ext', 'dimensionX', 'dimensionY', 'asset_date', 'added_date', 'createdAt', 'updatedAt']
    list_filter_multiples = ['ext', 'dimensionX', 'dimensionY', ]
    actions = ['collect']

    @button(type='danger', short_description='从icloud中获取数据', enable=True, confirm="您确定要生成吗？")
    def collect(self, request, queryset):
        th = threading.Thread(target=collect_all_medias)
        th.start()
        return {
            'state': True,
            'msg': f'采集程序已经启动'
        }
        #
        # messages.add_message(request, messages.DEBUG, '操作成功123123123123')
        # messages.add_message(request, messages.WARNING, '操作成功123123123123')
        # messages.add_message(request, messages.INFO, '操作成功123123123123')

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "size":
            if value:
                return human_readable_bytes(value)
        return value

    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '280px',
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
        'filename': {
            'width': '200px',
            'align': 'center'
        },
        'ext': {
            'width': '100px',
            'align': 'center'
        },
        'size': {
            'width': '120px',
            'align': 'center'
        },
        'dimensionX': {
            'width': '70px',
            'align': 'left'
        },
        'dimensionY': {
            'width': '70px',
            'align': 'left'
        },
        'asset_date': {
            'width': '180px',
            'align': 'left'
        },
        'added_date': {
            'width': '180px',
            'align': 'left'
        },
    }
