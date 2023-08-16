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
from ..models import IMedia, Album

iService = icloud.IcloudService(ICLOUD_USERNAME, ICLOUD_PASSWORD, True)


def collect_all_medias():
    all_photos = iService.photos.all
    total = len(all_photos)
    for i, p in enumerate(all_photos):
        fn, ext = os.path.splitext(p.filename)
        ext = str(ext).upper()
        obj = IMedia(id=p.id, filename=p.filename, ext=ext, size=p.size, dimensionX=p.dimensions[0],
                     dimensionY=p.dimensions[1], asset_date=p.asset_date, added_date=p.added_date,
                     versions=json.dumps(p.versions, indent=4, ensure_ascii=False))
        if ext in ['.MOV', '.MP4']:
            obj.video = p.versions['thumb']["url"]
        else:
            obj.img = p.versions['thumb']["url"]
        obj.save()
        print(f"{i / total * 100:.2f}%({i}/{total})", p.id)
        if p.created != p.asset_date:
            raise Exception("异常数据")
        # messages.add_message(request, messages.ERROR, '操作成功123123123123')


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['createdAt', 'updatedAt', 'name', 'total']
    list_filter = ['createdAt', 'updatedAt']
    actions = ['sync', 'collect']

    @button(type='danger', short_description='从icloud中同步相册列表', enable=True, confirm="您确定要生成吗？")
    def sync(self, request, queryset):
        for i, album_name in enumerate(iService.photos.albums):
            album = iService.photos.albums[album_name]
            total = len(album)
            print(i, album_name, total)
            obj = Album(name=album_name, total=total)
            obj.save()
        return {
            'state': True,
            'msg': f'同步成功'
        }

    @button(type='warning', short_description='同步媒体', enable=True, confirm="您确定要生成吗？")
    def collect(self, request, queryset):
        for i, qs in enumerate(queryset):
            print(i, qs)
        # th = threading.Thread(target=collect_all_medias)
        # th.start()
        return {
            'state': True,
            'msg': f'采集程序已经启动'
        }


@admin.register(IMedia)
class IMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename', 'ext', 'size', 'dimensionX', 'dimensionY', 'video', 'img', 'asset_date',
                    'added_date',
                    'createdAt', 'updatedAt']
    list_filter = ['ext', 'dimensionX', 'dimensionY', 'asset_date', 'added_date', 'createdAt', 'updatedAt']
    # list_filter_multiples = ('ext', 'dimensionX', 'dimensionY',)
    actions = ['collect', 'migrate']

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

    @button(type='warning', short_description='数据调整', enable=True, confirm="您确定要生成吗？")
    def migrate(self, request, queryset):
        for i, qs in enumerate(queryset):
            versions = json.loads(qs.versions)
            print(i, qs, versions)
            if qs.ext in ['.MOV', '.MP4']:
                qs.video = versions['thumb']["url"]
            else:
                qs.img = versions['thumb']["url"]
            qs.save()
        return {
            'state': True,
            'msg': f'调整成功！'
        }

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "size":
            if value:
                return f"""<span title="{value}">{human_readable_bytes(value)}</span>"""
        if field_name == 'img':
            if value:
                return f"""<img src="{value}" style="height:100px;">"""
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
        'img': {
            'width': '220px',
            'align': 'center'
        },
    }