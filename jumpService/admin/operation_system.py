# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/12/11
@Software: PyCharm
@disc:
======================================="""
import base64

from django.contrib import admin
from simplepro.admin import FieldOptions, BaseAdmin
from simplepro.dialog import ModalDialog

from ..models import OperationSystem, OperationSystemImage, SSHService


@admin.register(OperationSystemImage)
class OperationSystemImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'version', 'updatedAt', 'createdAt', 'deletedAt']
    fields_options = {
        'id': FieldOptions.UUID,
        'code': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'name': {
            'min_width': '280px',
            'align': 'left'
        },
        'version': {
            'min_width': '180px',
            'align': 'left'
        }
    }


@admin.register(OperationSystem)
class OperationSystemAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'server', 'rootUsername', 'rootPassword', 'open_webssh',
                    'updatedAt', 'createdAt', 'deletedAt']
    list_filter = ['image', 'server']
    search_fields = ['image', 'server']

    def open_webssh(self, obj: OperationSystem):
        modal = ModalDialog()
        modal.width = "1200"
        modal.height = "600"
        ips = obj.server.ips.all()
        ssh_services = obj.server.SSHServices.all()
        print("ssh_services:", ssh_services)
        ssh_port = 22
        if ssh_services.__len__() > 0:
            ssh_port = ssh_services[0].port
        if len(ips) > 0:
            # 这个是单元格显示的文本
            modal.cell = '<el-link type="primary">开始</el-link>'
            modal.title = "SSH安全远程链接"
            # Base64编码
            encoded_pwd = base64.b64encode(obj.rootPassword.encode('utf-8')).decode('utf-8')
            # 这里的url可以写死，也可以用django的反向获取url，可以根据model的数据，传到url中
            modal.url = "http://localhost:9080?hostname={}&port={}&username={}&password={}".format(ips[0].ip, ssh_port,
                                                                                                   obj.rootUsername,
                                                                                                   encoded_pwd)
            print("正在连接SSH", modal.url)
        else:
            modal.cell = ""
        # 是否显示取消按钮
        modal.show_cancel = True
        return modal

    open_webssh.short_description = "远程桌面/SSH"

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "ip":
            if value:
                return BaseAdmin.username(obj.ip)
        if field_name == 'rootPassword':
            if value:
                return BaseAdmin.password(obj.rootPassword)
        if field_name == "bios":
            if value:
                return BaseAdmin.password(obj.bios)
        return value

    fields_options = {
        'id': FieldOptions.UUID,
        'code': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'server': {
            'min_width': '280px',
            'align': 'left'
        },
        'net': {
            'min_width': '180px',
            'align': 'center'
        },
        'image': {
            'min_width': '160px',
            'align': 'left',
            "show_overflow_tooltip": True
        },
        'rootUsername': FieldOptions.USER_NAME,
        'rootPassword': FieldOptions.PASSWORD,
        'open_webssh': {
            'min_width': '120px',
            'align': 'center'
        },
        'hoster': {
            'min_width': '320px',
            'align': 'left'
        },
        'status': {
            'min_width': '180px',
            'align': 'left'
        },
        'remark': {
            'min_width': '200px',
            'align': 'left'
        },

        'bios': {
            'min_width': '180',
            'align': 'center'
        },
        'cabinet': {
            'min_width': '180',
            'align': 'center'
        },
        'mac': {
            'min_width': '220px',
            'align': 'left'
        }
    }
