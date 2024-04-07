# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/8/16
@Software: PyCharm
@disc:
======================================="""
import logging
import os.path
import threading
import urllib.parse
import uuid
from datetime import datetime
from urllib.parse import urlencode

from django.contrib import admin
from django.http import JsonResponse
from minio_storage.storage import get_setting
from simplepro.admin import FieldOptions
from simplepro.decorators import button, layer
from simplepro.dialog import MultipleCellDialog, ModalDialog
from simpleui.admin import AjaxAdmin

from utils import human_readable_bytes, human_readable_time, icloud
from .models import IMedia, Album, LocalMedia, AppleId
from .services import collect_all_medias, delete_from_icloud, migrateIcloudToLocal
from .views import DLT

iService: icloud.IcloudService = None


@admin.register(AppleId)
class AccountAdmin(AjaxAdmin):
    list_display = ['id', 'email', 'tel', 'passwd', 'last2FactorAuthenticateAt', 'last_2fa_time',
                    'isActive', 'lastConfirmedSessionValidityAt', 'maxSessionAge', 'updatedAt',
                    'createdAt']
    fields = ('email', 'tel', 'passwd', 'info')
    actions = ['two_factor_authenticate']

    def async_get_layer_config(self, request, queryset):
        """
        这个方法只有一个request参数，没有其他的入参
        """
        global iService
        qs: AppleId = queryset[0]
        print("被选中的用户名:", qs.username, qs.passwd)
        config = {
            # 弹出层中的输入框配置

            # 这里指定对话框的标题
            'title': '两步验证(Two Factor Authentication)',
            # 提示信息
            'tips': f'账号{qs.username}已经验证过！！！',
            # 确认按钮显示文本
            'confirm_button': '确认提交',
            # 取消按钮显示文本
            'cancel_button': '取消',

            # 弹出层对话框的宽度，默认50%
            'width': '40%',

            # 表单中 label的宽度，对应element-ui的 label-width，默认80px
            'labelWidth': "80px",
            'params': []
        }
        iService = icloud.IcloudService(qs.username, qs.passwd, True)
        print(f"连接成功！[{iService.requires_2fa}, {iService.requires_2sa}]")
        if iService.requires_2fa:
            config["tips"] = f"正在为账号{qs.username}进行两步验证.....\nTwo-factor authentication required."
            config["params"].append({
                # 这里的type 对应el-input的原生input属性，默认为input
                'type': 'input',
                # key 对应post参数中的key
                'key': 'code',
                # 显示的文本
                'label': '验证码',
                # 为空校验，默认为False
                'require': True,
                'extras': {
                    'prefix-icon': 'el-icon-delete',
                    'suffix-icon': 'el-icon-setting',
                    'clearable': True,
                    'placeholder': '请输入在你设备上出现6位验证码'
                }

            })
        else:
            qs.lastConfirmedSessionValidityAt = datetime.now()
            csa = qs.current_session_age
            if csa > qs.maxSessionAge:
                qs.maxSessionAge = csa
            qs.save()

        # elif iService.requires_2sa:
        #     print("进来了")
        #     config[
        #         "tips"] = f"正在为账号{qs.username}进行两步验证.....\nTwo-step authentication required. Your trusted devices are: (Which device would you like to use?)"
        #     # FIXME: 这里的设备无法获取， 估计是icloud升级了接口，而这个依赖库没有更新导致的
        #     devices = iService.trusted_devices
        #     print("守信任设备：", devices)
        #     options = []
        #     for i, device in enumerate(devices):
        #         opt = {
        #             'key': i,
        #             'label': device.get('deviceName', "SMS to %s" % device.get('phoneNumber'))
        #         }
        #         print(opt)
        #         options.append(opt)
        #     config["params"].append({
        #         # 这里的type 对应el-input的原生input属性，默认为input
        #         'type': 'select',
        #         # key 对应post参数中的key
        #         'key': 'device',
        #         # 显示的文本
        #         'label': '受信任设备',
        #         # 为空校验，默认为False
        #         'require': True,
        #         'options': options,
        #         'extras': {
        #             'prefix-icon': 'el-icon-delete',
        #             'suffix-icon': 'el-icon-setting',
        #             'clearable': True,
        #             "placeholder": "请选择受信任设备"
        #         }
        #
        #     })
        # 模拟处理业务耗时
        # 可以根据request的用户，来动态设置返回哪些字段，每次点击都会来获取配置显示
        print(config)
        return config

    def two_factor_authenticate(self, request, queryset):
        post = request.POST
        # 这里获取到数据后，可以做些业务处理
        # post中的_action 是方法名
        # post中 _selected 是选中的数据，逗号分割
        if not post.get('_selected'):
            return JsonResponse(data={
                'status': 'error',
                'msg': '没有选择任何AppleID！'
            })
            # device = devices[device]
            # if not self.send_verification_code(device):
            #     logging.error("Failed to send verification code")
            #
            # code = click.prompt('Please enter validation code')
            # if not self.validate_verification_code(device, code):
            #     logging.info("Failed to verify verification code")
        else:
            code = post.get("code")
            logging.info(f"用户输入的验证码：{code}")
            result = iService.validate_2fa_code(code)
            logging.info("Code validation result: %s" % result)
            if not result:
                logging.error("Failed to verify security code")
                return JsonResponse(data={
                    'status': 'error',
                    'msg': '验证码错误！'
                })
            if not iService.is_trusted_session:
                logging.warning("Session is not trusted. Requesting trust...")
                result = iService.trust_session()
                logging.info("Session trust result %s" % result)
                if not result:
                    logging.error(
                        "Failed to request trust. You will likely be prompted for the code again in the coming weeks")
                    return JsonResponse(data={
                        'status': 'error',
                        'msg': 'Failed to request trust. You will likely be prompted for the code again in the coming weeks！'
                    })
            appleId: AppleId = queryset[0]
            appleId.last2FactorAuthenticateAt = datetime.now()
            appleId.save()
            return JsonResponse(data={
                'status': 'success',
                'msg': '验证成功！'
            })

    two_factor_authenticate.short_description = "两步验证"
    two_factor_authenticate.icon = 'el-icon-view'
    two_factor_authenticate.layer = async_get_layer_config

    def isActive(self, obj: AppleId):
        global iService
        if iService is not None:
            if obj.username == iService.user.get("accountName"):
                return '<el-radio value="1" label="1">已被选中</el-radio>'
        else:
            return '<el-radio value="1" label="2"><a href="#">点击选择</a></el-radio>'

    isActive.short_description = "被选中"

    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '40px',
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
        'two_factor_authenticate': {
            'width': '100px',
            'align': 'center',
            'fixed': 'right'
        },
        'email': FieldOptions.EMAIL,
        'tel': FieldOptions.MOBILE,
        'last2FactorAuthenticateAt': FieldOptions.DATE_TIME,
        'last_2fa_time': FieldOptions.DURATION,
        'passwd': FieldOptions.DURATION,
        'lastConfirmedSessionValidityAt': {
            'width': "220px",
            'align': 'center'
        },
        'maxSessionAge': FieldOptions.DURATION,
        'isActive': {
            'width': '160px',
            'align': 'center'
        },
    }


def get_sync_layer_config(request, queryset):
    """
    这个方法只有一个request参数，没有其他的入参
    """
    options = []
    objs = AppleId.objects.all()
    for obj in objs:
        options.append({
            "label": obj.email,
            "key": obj.email
        })
    return {
        # 弹出层中的输入框配置

        # 这里指定对话框的标题
        'title': '相册数据同步',
        # 提示信息
        'tips': f'请选出一个账号用来同步数据！！！',
        # 确认按钮显示文本
        'confirm_button': '确认提交',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "160px",
        'params': [{
            # 这里的type 对应el-input的原生input属性，默认为input
            'type': 'select',
            # key 对应post参数中的key
            'key': 'apple_id',
            # 显示的文本
            'label': '要同步的iCloud账号',
            # 为空校验，默认为False
            'require': True,
            'options': options,
            'extras': {
                'prefix-icon': 'el-icon-delete',
                'suffix-icon': 'el-icon-setting',
                'clearable': True,
                "placeholder": "请选择受信任设备"
            }

        }]
    }


@admin.register(Album)
class AlbumAdmin(AjaxAdmin):
    list_display = ['id', 'name', 'total', 'count', 'synced', 'size',
                    'appleId',
                    'query_fieldName', 'query_comparator', 'query_fieldValue_type',
                    'query_fieldValue_value',
                    'updatedAt', 'createdAt', 'deletedAt'
                    ]
    list_filter = ['appleId', 'synced', 'createdAt', 'updatedAt', 'query_fieldName',
                   'query_comparator', 'query_fieldValue_type']
    actions = ['sync', 'collect', 'handle_pk']
    search_fields = ['name', 'query_fieldValue_value']
    ordering = ('-updatedAt',)

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

    @layer(config=get_sync_layer_config)
    @button(type='danger', short_description='从icloud中同步相册列表', enable=True, confirm="您确定要生成吗？")
    def sync(self, request, queryset):
        post = request.POST
        if not post.get('apple_id'):
            return JsonResponse(data={
                'status': 'error',
                'msg': '没有选择任何AppleID！'
            })
        else:
            apple_id = post.get("apple_id")
            qs: AppleId = AppleId.objects.filter(email=apple_id).first()
            print("被选中的用户名:", qs.username, qs.passwd)
            _iService = icloud.IcloudService(qs.username, qs.passwd, True)
            print(f"连接成功！[{_iService.requires_2fa}, {_iService.requires_2sa}]")
            if _iService.requires_2fa:
                return JsonResponse(data={
                    'status': 'warn',
                    'msg': '需要先去做二次验证, 此页面无法验证'
                })
            else:
                for i, album_name in enumerate(_iService.photos.albums):
                    album = _iService.photos.albums[album_name]
                    total = len(album)
                    print(i, album_name, total, album.query_filter)
                    obj, _ = Album.objects.get_or_create(name=album_name, appleId=apple_id)
                    obj.total = total
                    obj.agg()
                    obj.set_query(album.query_filter)
                    obj.appleId = apple_id
                    obj.save()
                return {
                    'state': True,
                    'msg': f'同步成功'
                }

    @button(type='warning', short_description='同步媒体', enable=False, confirm="您确定要生成吗？")
    def collect(self, request, queryset):
        for qs in queryset:
            # FIXME: 以下调用的 collect_all_media 方法, 目前只接受一个参数iService,
            #  所以不支持按照输入的album来同步, 需要继续实现.
            th = threading.Thread(target=collect_all_medias, args=([qs],))
            th.start()
        return {
            'state': True,
            'msg': f'采集程序已经启动'
        }

    @button(type='warning', short_description='处理PK', enable=True, confirm="确定对PK进行特殊处理吗?")
    def handle_pk(self, request, queryset):
        for i, album in enumerate(Album.objects.all()):
            final_pk = None
            if album.query_fieldValue_value == "" or album.query_fieldValue_value is None:
                final_pk = uuid.uuid4().__str__()
            else:
                final_pk = album.query_fieldValue_value
            print(f"album{i}:{album.name} ===> {final_pk}")
            album.id = final_pk
            album.save()
            medias = album.medias.all()
            for j, media in enumerate(medias):
                print(" " * 10, "|", "-" * 10, f"{j}/{media.__len__()}", media, "===>", final_pk)
        return {
            'state': True,
            'msg': f'处理成功'
        }

    fields_options = {
        'id': FieldOptions.UUID,
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
            'align': 'left'
        },
        'total': {
            'width': '100px',
            'align': 'right'
        },
        'count': {
            'width': '120px',
            'align': 'right'
        },
        'synced': {
            'width': '70px',
            'align': 'right'
        },
        'size': {
            'width': '100px',
            'align': 'right'
        },
        'appleId': {
            'width': '120px',
            'align': 'right',
            "show_overflow_tooltip": True
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


class ThumbFilter(admin.SimpleListFilter):
    title = '缩略图'  # 过滤器标题
    parameter_name = 'thumb'  # URL中参数的名字

    def lookups(self, request, model_admin):
        # 返回要显示为过滤选项的值
        a = LocalMedia.objects.filter(thumb__isnull=False).count()
        b = LocalMedia.objects.filter(thumb__isnull=True).count()
        return [(0, f"有({a})"), (1, f"无({b})")]

    def queryset(self, request, queryset):
        # 对查询集进行过滤
        if self.value() == '0':
            return queryset.filter(thumb__isnull=False)
        elif self.value() == '1':
            return queryset.filter(thumb__isnull=True)
        else:
            return queryset.filter()


class PrvFilter(admin.SimpleListFilter):
    title = '可预览文件'  # 过滤器标题
    parameter_name = 'prv_f'  # URL中参数的名字

    def lookups(self, request, model_admin):
        # 返回要显示为过滤选项的值
        return [(0, f"有"), (1, f"无")]
        # FIXME: 自从引入MinIO之后,此功能就无法正常使用了, 请尽快修复相关功能
        a = 0
        b = 0
        for i in LocalMedia.objects.all():
            if i.prv:
                try:
                    if os.path.exists(i.prv.path):
                        a += 1
                    else:
                        b += 1
                except ValueError as e:
                    if "The 'prv' attribute has no file associated with it." in str(e):
                        b += 1
            else:
                pass
        return [(0, f"有({a})"), (1, f"无({b})")]

    def queryset(self, request, queryset):
        # 对查询集进行过滤
        id_list = []
        if self.value() == '0':
            for i in IMedia.objects.all():
                try:
                    if os.path.exists(i.prv.path):
                        id_list.append(i.id)
                except ValueError as e:
                    if "The 'prv' attribute has no file associated with it." in str(e):
                        pass
            return queryset.filter(id__in=id_list)
        elif self.value() == '1':
            for i in IMedia.objects.all():
                try:
                    if not os.path.exists(i.prv.path):
                        id_list.append(i.id)
                except ValueError as e:
                    if "The 'prv' attribute has no file associated with it." in str(e):
                        id_list.append(i.id)
            return queryset.filter(id__in=id_list)
        else:
            return queryset.filter()


@admin.register(IMedia)
class IMediaAdmin(AjaxAdmin):
    list_display = ['id', 'startRank', 'filename', 'ext', 'size', 'duration', 'thumb', 'dialog_lists',
                    'dimensionX', 'dimensionY',
                    'isHidden', 'isFavorite', 'deleted',
                    'asset_date', 'added_date', 'createdAt', 'updatedAt',
                    'adjustmentRenderType', 'timeZoneOffset', 'burstFlags',
                    'orientation',
                    'masterRecordType', 'assetRecordType',
                    'masterRecordChangeTag', 'assetRecordChangeTag',
                    'createdDeviceID', 'createdUserRecordName', 'modifiedDeviceID', 'modifiedUserRecordName',
                    'locationEnc']
    list_filter = ['albums', 'ext', 'dimensionX', 'dimensionY', 'asset_date', 'added_date', 'createdAt',
                   'updatedAt', 'isHidden', 'isFavorite', 'deleted',
                   'createdDeviceID', 'createdUserRecordName', 'modifiedDeviceID', 'modifiedUserRecordName',
                   'adjustmentRenderType', 'timeZoneOffset', 'burstFlags',
                   'orientation',
                   'masterRecordChangeTag', 'assetRecordChangeTag',
                   'masterRecordType', 'assetRecordType'
                   ]  # TODO:实现是否为实况图的过滤器，可以通过originalRes.ext和prv.ext来确认。
    # list_filter_multiples = ('ext', 'dimensionX', 'dimensionY',)
    search_fields = ['id', 'filename']
    actions = ['collect', 'migrate', 'delete']
    list_per_page = 20

    def thumb(self, obj):
        thumb_url = obj.thumbURL
        prv_url = "https://cvws.icloud-content.com.cn/B/AXsCTFGEAH5K_G8v5M550BKYQgrYAU3Llil8eeGq1YllzSOChTP8GzK8/$%7Bf%7D?o=AtJgOCoyIAwQaAoS4iNMm_t_66U9m_Cwk6V-Xc5u9itt&v=1&x=3&a=CAogEuXMIhmVlMSdUwyDPmMEeHBW4Pe8dlT5llye-A7y1KUSbxCh0t6dqTEYoa-6n6kxIgEAUgSYQgrYWgT8GzK8aicHbBtuls-GzfByFYWw_IFgUTD-mns3AcGQtUB2RN2ncMsWk2-ItNJyJ7ksv1IBrE1ycr9kwjX2z7yo1W7T6a5KGQ4z8-32UP5ONKX9XWGyHw&e=1694699001&fl=&r=65210c2f-4722-49e5-9724-3e53321d48d7-1&k=4uaX3YNtEyqLkhukOc7y5A&ckc=com.apple.photos.cloud&ckz=PrimarySync&y=1&p=215&s=bsmRo--bR8qyGg-VJt0rZnR_1XI"
        dlt = datetime.now() - obj.updatedAt
        if dlt > DLT:
            thumb_url = f"/icloud/thumb?" + urlencode({"id": obj.id, "startRank": obj.startRank})
        return '''<el-image style="width: 100px; height: 100px" src="{}" :preview-src-list="['{}']" lazy></el-image>'''.format(
            thumb_url, thumb_url)

    thumb.short_description = "缩略图"

    def dialog_lists(self, model):
        return MultipleCellDialog([
            ModalDialog(url=f'/static/preview.html?id={urllib.parse.quote(model.id)}&source=IMedia',
                        title=model.filename,
                        cell='<el-link type="primary">预览</el-link>', width="840px", height="600px"),
        ])

    # 这个是列头显示的文本
    dialog_lists.short_description = "预览"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # groupList = []
        # start = queryset[0].startRank
        # group = []
        # n = 0
        # for qs in queryset:
        #     distance = qs.startRank - start
        #     if distance < 100:
        #         group.append(qs)
        #     else:
        #         groupList.append(group)
        #         n += 1
        #         print(n, group[0].startRank, "~", group[-1].startRank, len(group))
        #         group = [qs]
        #         start = qs.startRank
        return queryset

    def get_paginator(self, request, queryset, per_page, orphans=0, allow_empty_first_page=True):
        res = super().get_paginator(request, queryset, per_page, orphans, allow_empty_first_page)
        return res

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
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    @layer(config=get_sync_layer_config)
    @button(type='danger', short_description='从icloud中获取数据', enable=True, confirm="您确定要生成吗？")
    def collect(self, request, queryset):
        post = request.POST
        if not post.get('apple_id'):
            return JsonResponse(data={
                'status': 'error',
                'msg': '没有选择任何AppleID！'
            })
        else:
            apple_id = post.get("apple_id")
            qs: AppleId = AppleId.objects.filter(email=apple_id).first()
            print("被选中的用户名:", qs.username, qs.passwd)
            _iService = icloud.IcloudService(qs.username, qs.passwd, True)
            print(f"连接成功！[{_iService.requires_2fa}, {_iService.requires_2sa}]")
            if _iService.requires_2fa:
                return JsonResponse(data={
                    'status': 'warn',
                    'msg': '需要先去做二次验证, 此页面无法验证'
                })
            else:
                th = threading.Thread(target=collect_all_medias, args=(_iService,))
                th.start()
                return {
                    'state': True,
                    'msg': f'采集程序已经启动'
                }

    @button(type='warning', short_description='数据迁移', enable=False, confirm="您确定从icloud迁移到本地吗？")
    def migrate(self, request, queryset):
        ids = request.POST.get('ids').replace(" ", "+").split(",")
        objs = IMedia.objects.filter(id__in=ids).all()
        for i, qs in enumerate(objs):
            migrateIcloudToLocal(qs)
        return {
            'state': True,
            'msg': f'迁移开始！'
        }

    @button(type='error', short_description='从iCloud中删除', enable=False, confirm="您确定从icloud迁移到本地吗？")
    def delete(self, request, queryset):
        ids = request.POST.get('ids').replace(" ", "+").split(",")
        objs = IMedia.objects.filter(id__in=ids).all()
        for qs in objs:
            lm = LocalMedia.objects.filter(id=qs.id).first()
            resp = delete_from_icloud(qs, lm)
            return {
                'state': True,
                'msg': resp.text
            }

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "size":
            if value:
                return f"""<span title="{value}">{human_readable_bytes(value)}</span>"""
        if field_name == 'img':
            if value:
                return f"""<img src="{value}" style="height:100px;">"""
        if field_name == "duration":
            if value:
                return f"""<span title="{value}">{human_readable_time(value)}</span>"""
        return value

    fields_options = {
        'id': {
            # 'fixed': 'left',
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
        'thumb': {
            'width': '130px',
            'align': 'center'
        },
        'duration': {
            'width': '130px',
            'align': 'center'
        },
        'createdUserRecordName': {
            'width': '300px',
            'align': 'left'
        },
        'modifiedUserRecordName': {
            'width': '300px',
            'align': 'left'
        },
        'createdDeviceID': {
            'width': '400px',
            'align': 'left'
        },
        'modifiedDeviceID': {
            'width': '400px',
            'align': 'left'
        },
        'locationEnc': {
            'width': '1000px',
            'align': 'left'
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


@admin.register(LocalMedia)
class LocalMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename', 'ext', 'size', 'thumb', 'dialog_lists', 'dimensionX', 'dimensionY',
                    'asset_date', 'added_date', 'detach_icloud_date', 'createdAt', 'updatedAt', 'origin'
                    ]
    list_filter = ['ext', 'dimensionX', 'dimensionY', 'asset_date', 'added_date', 'createdAt', 'updatedAt',
                   ThumbFilter, PrvFilter]  # TODO:实现是否为实况图的过滤器，可以通过originalRes.ext和prv.ext来确认。
    # list_filter_multiples = ('ext', 'dimensionX', 'dimensionY',)
    search_fields = ['id', 'filename']
    actions = []
    list_per_page = 20

    def dialog_lists(self, model):
        return MultipleCellDialog([
            ModalDialog(url=f'/icloud/detail?id={urllib.parse.quote(model.id)}&source=LocalMedia', title=model.filename,
                        cell='<el-link type="primary">预览</el-link>', width="840px", height="600px"),
        ])

    def _thumb(self, obj):
        if obj.prv.name is None:
            return True
        return False

    # 这个是列头显示的文本
    dialog_lists.short_description = "预览"

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "size":
            if value:
                return f"""<span title="{value}">{human_readable_bytes(value)}</span>"""
        if field_name == 'thumb':
            if value:
                # STORAGE_END_POINT = get_setting("MINIO_STORAGE_ENDPOINT")
                # BUCKET_NAME = get_setting("MINIO_STORAGE_MEDIA_BUCKET_NAME")
                final_url = "/media/" + value
                # print(STORAGE_END_POINT, print(final_url))
                return f"""<el-image src="{final_url}" style="height:100px;" :preview-src-list="['{final_url}']" lazy >"""
        if field_name == "duration":
            if value:
                return f"""<span title="{value}">{human_readable_time(value)}</span>"""
        if field_name == "origin":
            if value:
                return f""" <el-link type="primary" href="/media/{value}" target="_blank">点击浏览源文件</el-link>"""
        return value

    fields_options = {
        'id': {
            # 'fixed': 'left',
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
            'align': 'center'
        },
        'added_date': {
            'width': '180px',
            'align': 'center'
        },
        'thumb': {
            'width': '120px',
            'align': 'center'
        },
        'origin': {
            'width': '200px',
            'align': 'center'
        },
        'detach_icloud_date': {
            'width': '180px',
            'align': 'center'
        }
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
