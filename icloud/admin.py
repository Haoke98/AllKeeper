# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/8/16
@Software: PyCharm
@disc:
======================================="""
import datetime
import json
import logging
import math
import os.path
import threading
import time
import traceback
import urllib.parse

import requests
from django.contrib import admin
from django.core.files.base import ContentFile
from simplepro.decorators import button
from simplepro.dialog import MultipleCellDialog, ModalDialog

from lib import human_readable_bytes
from . import iService
from .models import IMedia, Album

STATUS_FINISHED = "FINISHED"
STATUS_STOP = "STOPPING"
STATUS_RUNNING = "Running"
STATUS_EXCEPTION = "Exception"
STATUS = STATUS_STOP

TOTAL = -1
FINISHED_COUNT = 0
STARTED_AT = datetime.datetime.now()
EXCEPTION_MSG = None
EXCEPTION_TRACE_BACK = None


def download_thumb(obj: IMedia, p):
    fields = p._master_record['fields']
    if fields.keys().__contains__("resJPEGThumbRes"):
        downloadURL = fields['resJPEGThumbRes']['value']['downloadURL']
        thumbResp = requests.get(downloadURL)
        thumbCF = ContentFile(thumbResp.content, f"{p.filename}.JPG")
        obj.thumb = thumbCF
        obj.save()


def download_prv(obj: IMedia, p):
    fields: dict = p._master_record['fields']
    if fields.keys().__contains__("resVidSmallRes"):
        downloadURL = fields['resVidSmallRes']['value']['downloadURL']
        resp = requests.get(downloadURL)
        cf = ContentFile(resp.content, f"{p.filename}.MP4")
        obj.prv_file = cf
        obj.save()
    else:
        # 由于图片的预览文件和Thumb缩略图一样，所以不用再重新下载
        pass


def insert_or_update_media(p):
    fn, ext = os.path.splitext(p.filename)
    ext = str(ext).upper()
    startedAt1 = time.time()
    obj, created = IMedia.objects.get_or_create(id=p.id)
    print(f"查询[{obj.id}]成功！[Created:{created},Duration:{time.time() - startedAt1} s]")
    startedAt2 = time.time()
    if created:
        obj.filename = p.filename
        obj.ext = ext
        obj.size = p.size
        obj.dimensionX = p.dimensions[0]
        obj.dimensionY = p.dimensions[1]
        obj.asset_date = p.asset_date
        obj.added_date = p.added_date
        download_thumb(obj, p)
        download_prv(obj, p)
    else:
        obj.versions = json.dumps(p.versions, indent=4, ensure_ascii=False)
        try:
            if obj.thumb or not os.path.exists(obj.thumb.path):
                download_thumb(obj, p)
        except ValueError as e:
            if "The 'thumb' attribute has no file associated with it." in str(e):
                download_thumb(obj, p)
            else:
                raise ValueError(e)
        try:
            if obj.prv_file or not os.path.exists(obj.prv_file.path):
                download_prv(obj, p)
        except ValueError as e:
            if "The 'prv_file' attribute has no file associated with it." in str(e):
                download_prv(obj, p)
            else:
                raise ValueError(e)
    print(f"预处理[{obj.id}]成功！[Duration:{time.time() - startedAt2} s]")
    startedAt3 = time.time()
    obj.save()
    print(f"保存[{obj.id}]成功！[Duration:{time.time() - startedAt3} s]")
    return obj


def collect(p, album, i, total):
    if p.created != p.asset_date:
        raise Exception("异常数据")
    try:
        obj = insert_or_update_media(p)
        obj.albums.add(album)
        obj.save()
        print(f"{album.name}: {(i + 1) / total * 100:.2f}%({i + 1}/{total}), {obj}")
        return obj
    except Exception as e:
        logging.error(f"异常：{e}: {traceback.format_exc()}")
        return None


def collect_all_medias():
    global STATUS, FINISHED_COUNT, TOTAL, STARTED_AT, EXCEPTION_MSG, EXCEPTION_TRACE_BACK
    # for album in albums:
    #     photos = iService.photos.albums[album.name]
    #     total = len(photos)
    # if album.count == total:
    #     print(f"{album.name}: 无需同步跳过")
    #     continue
    # for i, p in enumerate(photos):
    #     th = threading.Thread(target=collect, args=(p, album, i, total))
    #     th.start()
    # album.agg()
    # album.save()
    # target_photo = None
    STATUS = STATUS_RUNNING
    STARTED_AT = datetime.datetime.now()
    try:
        medias = iService.photos.all
        TOTAL = len(medias)
        FINISHED_COUNT = 0
        for i, photo in enumerate(medias):
            FINISHED_COUNT = i + 1
            progress = FINISHED_COUNT / TOTAL * 100
            dlt = datetime.datetime.now() - STARTED_AT
            finishedCount = math.ceil(TOTAL * progress / 100)
            speed_in_second = finishedCount / dlt.total_seconds()
            left = TOTAL - finishedCount
            dlt_in_second = left / speed_in_second
            dlt1 = datetime.timedelta(seconds=dlt_in_second)
            willFinishedAt = datetime.datetime.now() + dlt1
            startedAt = time.time()
            insert_or_update_media(photo)
            print(f"{progress:.2f}% ({FINISHED_COUNT}/{TOTAL}), {photo}, [Duration:{time.time() - startedAt} s]")
        STATUS = STATUS_FINISHED
    except Exception as e:
        STATUS = STATUS_EXCEPTION
        EXCEPTION_MSG = str(e)
        EXCEPTION_TRACE_BACK = traceback.format_exc()
        logging.error("iCloud数据同步异常", exc_info=True)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['createdAt', 'updatedAt', 'name', 'total', 'count', 'synced', 'size', 'query_fieldName',
                    'query_comparator', 'query_fieldValue_type', 'query_fieldValue_value']
    list_filter = ['synced', 'createdAt', 'updatedAt', 'query_fieldName',
                   'query_comparator', 'query_fieldValue_type']
    actions = ['sync', 'collect']
    search_fields = ['name', 'query_fieldValue_value']

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

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
            print(i, album_name, total, album.query_filter)
            obj, _ = Album.objects.get_or_create(name=album_name)
            obj.total = total
            obj.agg()
            obj.set_query(album.query_filter)
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
        'name': {
            'width': '180px',
            'align': 'center'
        },
        'total': {
            'width': '100px',
            'align': 'center'
        },
        'count': {
            'width': '120px',
            'align': 'center'
        },
        'synced': {
            'width': '70px',
            'align': 'left'
        },
        'size': {
            'width': '100px',
            'align': 'left'
        },
        'query_fieldName': {
            'width': '100px',
            'align': 'center'
        },
        'query_comparator': {
            'width': '100px',
            'align': 'center'
        },
        'query_fieldValue_type': {
            'width': '140px',
            'align': 'center'
        },
        'query_fieldValue_value': {
            'width': '340px',
            'align': 'center'
        },
    }


@admin.register(IMedia)
class IMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename', 'ext', 'size', 'dimensionX', 'dimensionY', 'thumb', 'dialog_lists'
        , 'asset_date',
                    'added_date',
                    'createdAt', 'updatedAt']
    list_filter = ['albums', 'ext', 'dimensionX', 'dimensionY', 'asset_date', 'added_date', 'createdAt', 'updatedAt']
    # list_filter_multiples = ('ext', 'dimensionX', 'dimensionY',)
    search_fields = ['id', 'filename']
    actions = ['collect', 'migrate']
    list_per_page = 20

    def dialog_lists(self, model):
        return MultipleCellDialog([
            ModalDialog(url=f'/icloud/detail?id={urllib.parse.quote(model.id)}', title=model.filename,
                        cell='<el-link type="primary">预览</el-link>', width="840px", height="600px"),
        ])

    # 这个是列头显示的文本
    dialog_lists.short_description = "预览"

    # 也可以是方法的形式来返回html
    def get_top_html(self, request):
        return f'''
        <el-collapse accordion>
            <el-collapse-item>
                <template slot="title">
                    同步进度监控<i class="header-icon el-icon-info"></i>
                </template>
                <iframe style="width:100%;height:200px;" src="/static/iMedia_list_top.html"></iframe>
            </el-collapse-item>
        </el-collapse>
        '''

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @button(type='danger', short_description='从icloud中获取数据', enable=True, confirm="您确定要生成吗？")
    def collect(self, request, queryset):
        th = threading.Thread(target=collect_all_medias)
        th.start()
        return {
            'state': True,
            'msg': f'采集程序已经启动'
        }

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
