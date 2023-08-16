# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/8/16
@Software: PyCharm
@disc:
======================================="""
import json
import logging
import os.path
import threading
import time
import traceback

from django.contrib import admin
from simplepro.decorators import button
from simplepro.dialog import MultipleCellDialog, ModalDialog

from izBasar.secret import ICLOUD_USERNAME, ICLOUD_PASSWORD
from lib import icloud, human_readable_bytes
from ..models import IMedia, Album

iService = icloud.IcloudService(ICLOUD_USERNAME, ICLOUD_PASSWORD, True)


def collect(p, album):
    if p.created != p.asset_date:
        raise Exception("异常数据")
    try:
        fn, ext = os.path.splitext(p.filename)
        ext = str(ext).upper()
        obj = IMedia(id=p.id, filename=p.filename, ext=ext, size=p.size, dimensionX=p.dimensions[0],
                     dimensionY=p.dimensions[1], asset_date=p.asset_date, added_date=p.added_date,
                     versions=json.dumps(p.versions, indent=4, ensure_ascii=False))
        obj.albums.add(album)
        # if ext in ['.MOV', '.MP4']:
        #     obj.video = p.versions['thumb']["url"]
        # else:
        #     obj.img = p.versions['thumb']["url"]
        obj.save()
        return obj
    except Exception as e:
        logging.error(f"异常：{e}: {traceback.format_exc()}")
        return None


def collect_all_medias(albums: list):
    for album in albums:
        photos = iService.photos.albums[album.name]
        total = len(photos)
        if album.count == total:
            print(f"{album.name}: 无需同步跳过")
            continue
        n = 0
        while True:
            for i, p in enumerate(photos):
                obj = collect(p, album)
                print(f"{album.name}: {(i + 1) / total * 100:.2f}%({i + 1}/{total}), {obj}")
                if i % 20 == 0:
                    album.agg()
                album.save()
            album.agg()
            album.save()
            if album.count == total:
                break
            else:
                n += 1
                if n == 3:
                    break
                time.sleep(2)

        # messages.add_message(request, messages.ERROR, '操作成功123123123123')


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['createdAt', 'updatedAt', 'name', 'total', 'count', 'synced', 'size']
    list_filter = ['synced', 'createdAt', 'updatedAt']
    actions = ['sync', 'collect']
    search_fields = ['name']

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "size":
            if value:
                return f"""<span title="{value}">{human_readable_bytes(value)}</span>"""
        return value

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
        for qs in queryset:
            th = threading.Thread(target=collect_all_medias, args=([qs],))
            th.start()
        return {
            'state': True,
            'msg': f'采集程序已经启动'
        }


@admin.register(IMedia)
class IMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename', 'ext', 'size', 'dimensionX', 'dimensionY', 'dialog_lists'
        , 'asset_date',
                    'added_date',
                    'createdAt', 'updatedAt']
    list_filter = ['albums', 'ext', 'dimensionX', 'dimensionY', 'asset_date', 'added_date', 'createdAt', 'updatedAt']
    # list_filter_multiples = ('ext', 'dimensionX', 'dimensionY',)
    search_fields = ['id', 'filename']
    actions = ['collect', 'migrate']

    def dialog_lists(self, model):
        return MultipleCellDialog([
            ModalDialog(url='https://simpleui.72wo.com/docs/simplepro', title=model.filename,
                        cell='<el-link type="primary">预览</el-link>', width="800px", height="500px"),
        ])

    # 这个是列头显示的文本
    dialog_lists.short_description = "预览"

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

    def layer_input(self, request, queryset):
        # 这里的queryset 会有数据过滤，只包含选中的数据

        post = request.POST
        # 这里获取到数据后，可以做些业务处理
        # post中的_action 是方法名
        # post中 _selected 是选中的数据，逗号分割
        if not post.get('_selected'):
            return JsonResponse(data={
                'status': 'error',
                'msg': '请先选中数据！'
            })
        else:
            return JsonResponse(data={
                'status': 'success',
                'msg': '处理成功！'
            })

    layer_input.short_description = '弹出对话框输入'
    layer_input.type = 'success'
    layer_input.icon = 'el-icon-s-promotion'

    # 指定一个输入参数，应该是一个数组

    # 指定为弹出层，这个参数最关键
    layer_input.layer = {
        # 弹出层中的输入框配置

        # 这里指定对话框的标题
        'title': '弹出层输入框',
        # 提示信息
        'tips': '这个弹出对话框是需要在admin中进行定义，数据新增编辑等功能，需要自己来实现。',
        # 确认按钮显示文本
        'confirm_button': '确认提交',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "80px",
        'params': [{
            # 这里的type 对应el-input的原生input属性，默认为input
            'type': 'input',
            # key 对应post参数中的key
            'key': 'name',
            # 显示的文本
            'label': '名称',
            # 为空校验，默认为False
            'require': True,
            # 附加参数
            'extras': {
                'prefix-icon': 'el-icon-delete',
                'suffix-icon': 'el-icon-setting',
                'clearable': True
            }
        }, {
            'type': 'select',
            'key': 'type',
            'label': '类型',
            'width': '200px',
            # size对应elementui的size，取值为：medium / small / mini
            'size': 'small',
            # value字段可以指定默认值
            'value': '0',
            'options': [{
                'key': '0',
                'label': '收入'
            }, {
                'key': '1',
                'label': '支出'
            }]
        }, {
            'type': 'number',
            'key': 'money',
            'label': '金额',
            # 设置默认值
            'value': 1000
        }, {
            'type': 'date',
            'key': 'date',
            'label': '日期',
        }, {
            'type': 'datetime',
            'key': 'datetime',
            'label': '时间',
        }, {
            'type': 'rate',
            'key': 'star',
            'label': '评价等级'
        }, {
            'type': 'color',
            'key': 'color',
            'label': '颜色'
        }, {
            'type': 'slider',
            'key': 'slider',
            'label': '滑块'
        }, {
            'type': 'switch',
            'key': 'switch',
            'label': 'switch开关'
        }, {
            'type': 'input_number',
            'key': 'input_number',
            'label': 'input number'
        }, {
            'type': 'checkbox',
            'key': 'checkbox',
            # 必须指定默认值
            'value': [],
            'label': '复选框',
            'options': [{
                'key': '0',
                'label': '收入'
            }, {
                'key': '1',
                'label': '支出'
            }, {
                'key': '2',
                'label': '收益'
            }]
        }, {
            'type': 'radio',
            'key': 'radio',
            'label': '单选框',
            'options': [{
                'key': '0',
                'label': '收入'
            }, {
                'key': '1',
                'label': '支出'
            }, {
                'key': '2',
                'label': '收益'
            }]
        }]
    }
