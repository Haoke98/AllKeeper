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
from simplepro.dialog import ModalDialog, MultipleCellDialog

from ..models import OperationSystem, OperationSystemImage, SSHService, IPAddress


@admin.register(OperationSystemImage)
class OperationSystemImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'version', 'arch', 'isLTS', 'updatedAt', 'createdAt', 'deletedAt']
    list_filter = ['name', 'arch', 'isLTS', 'updatedAt', 'createdAt']
    search_fields = ['version', 'remark']
    ordering = ['-updatedAt']
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
        },
        'arch': {
            'min_width': '100px',
            'align': 'left'
        },
    }


@admin.register(OperationSystem)
class OperationSystemAdmin(BaseAdmin):
    list_display = ['id', 'image', 'server', 'rootUsername', 'rootPassword', 'open_webssh',
                    'updatedAt', 'createdAt', 'deletedAt']
    list_filter = ['server', 'image', 'server__remark']
    search_fields = ['image', 'server']
    ordering = ('-updatedAt',)

    def open_webssh(self, obj: OperationSystem):

        modals = []

        def generate_modal(_ip: IPAddress, _port: int):
            # FIXME:影响列表页的渲染, 增加延迟, 需要改成固定, 让用户在单个item的详情页里进行渲染, 在详情页中选入口/切换入口
            print("ip:", _ip)
            prefix = "入口"
            if _ip.net is not None:
                if _ip.net.is_global():
                    prefix = "公网"
                else:
                    prefix = "内网"
            modal = ModalDialog()
            modal.width = "1200"
            modal.height = "600"
            # 这个是单元格显示的文本
            modal.cell = f'<el-link type="primary">{prefix}{len(modals) + 1}</el-link>'
            modal.title = "SSH安全远程链接"
            # 是否显示取消按钮
            modal.show_cancel = True
            # Base64编码
            encoded_pwd = base64.b64encode(obj.rootPassword.encode('utf-8')).decode('utf-8')
            # FIXME: [高危敏感信息泄漏漏洞] 必须即使改成后端创建session后,再从前端通过session访问.
            # 这里的url可以写死，也可以用django的反向获取url，可以根据model的数据，传到url中
            modal.url = "http://localhost:9080?hostname={}&port={}&username={}&password={}".format(_ip.ip, _port,
                                                                                                   obj.rootUsername,
                                                                                                   encoded_pwd)
            print("正在连接SSH", modal.url)
            modals.append(modal)

        ips = obj.server.ips.all()
        ssh_services = obj.server.SSHServices.all()
        print("ssh_services:", ssh_services)
        ssh_port = 22
        if ssh_services.__len__() > 0:
            ssh_port = ssh_services[0].port
        for ip in ips:
            generate_modal(ip, ssh_port)
        # TODO: 实现通过 lanproxy 的 API 实时创建端口映射关系.
        #  可以先查看有没有和当前服务器处在同一个网段的 lanproxy客户端, 也就是有没有可用的channels
        port_maps = obj.server.right_ports.all()
        for i, port_map in enumerate(port_maps):
            if i == 0:
                print("port_map:")
            if port_map.rightPort == ssh_port:
                print(" " * 10, "|", "-" * 10, f"{i}.", port_map)
                _ips = port_map.left.ips.all()
                for ip in _ips:
                    generate_modal(ip, port_map.leftPort)
        return MultipleCellDialog(modals)

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
