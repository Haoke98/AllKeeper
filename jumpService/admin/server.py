import errno
import socket
import threading

from django.contrib import admin
from django.db.models import QuerySet
from simplepro.admin import BaseAdmin, FieldOptions
from simplepro.decorators import button

from .net import IPAddressInlineAdmin
from ..models import ServerNew, IPAddress, ServerCabinet, ServerRoom, OperationSystem, OperationSystemImage, \
    DeviceStatus, ServerStatus


def sync_device_status():
    port = 80
    for i, obj in enumerate(ServerNew.objects.all()):
        for ip in obj.ips.all():
            try:
                # 创建socket对象
                sock = socket.create_connection((ip.ip, port), timeout=5)
                print(f"服务器 {ip.ip}:{port} 已经启动.")
                sock.close()
                ds = DeviceStatus(content="✅", device=obj, ip=ip.ip)
                ds.save()
            except socket.error as e:
                print(f"无法连接到服务器 {ip.ip}:{port}. 错误信息: {e}")
                if e.errno == errno.ECONNREFUSED:
                    ds = DeviceStatus(content="✅⚠️", device=obj, ip=ip.ip, errstr=str(e), errno=e.errno)
                    ds.save()
                else:
                    ds = DeviceStatus("❌", device=obj, ip=ip.ip, errstr=str(e), errno=e.errno)
                    ds.save()


@admin.register(ServerStatus)
class ServerStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'server', 'ip', 'cpuUsage', 'memoryUsage', 'diskUsage', 'createdAt']
    list_filter = ['server', 'ip', 'createdAt']
    search_fields = ['id', 'ip']


@admin.register(ServerNew)
class ServerAdmin(BaseAdmin):
    list_display = ["id", 'code', 'system_count', 'bios', 'cabinet', 'remark', 'hoster',
                    "mac", "updatedAt", "createdAt", "deletedAt"
                    ]
    list_display_links = ['remark', 'hoster']
    list_filter = ['hoster', 'cabinet__room', 'cabinet', 'updatedAt', 'createdAt', 'deletedAt']
    search_fields = ['remark', 'code']
    search_help_text = ['你好，这是搜索帮助语句！']
    autocomplete_fields = []
    list_per_page = 10
    fields = ['code', 'cabinet', 'hoster', 'bios', 'mac', 'remark', 'info']
    actions = ['sync', 'migrate', 'sync_status']
    inlines = [IPAddressInlineAdmin]
    ordering = ('-updatedAt',)

    # inlines = [ServerUserInlineAdmin]
    @button(type='danger', short_description='同步状态', enable=True)
    def sync_status(self, request, queryset):
        """
        同步状态
        :param obj:
        :return:
        """
        th = threading.Thread(target=sync_device_status, args=())
        th.start()
        return {
            'state': True,
            'msg': f'同步已开始'
        }

    @button(type='danger', short_description='新旧数据同步', enable=True, confirm="您确定要生成吗？")
    def sync(self, request, queryset):
        iService = None
        for i, oldServer in enumerate(Server.objects.all()):
            # net = Net.objects.get_or_create(content=)
            obj = ServerNew(
                id=oldServer.id,
                code=oldServer.code,
                rootUsername=oldServer.rootUsername,
                rootPassword=oldServer.rootPassword,
                hoster=oldServer.hoster,
                system=oldServer.system,
                status=oldServer.status,
                bios=oldServer.bios,
                ssh=oldServer.ssh,
                mac=oldServer.mac,
                remark=oldServer.remark
            )
            obj.save()
            net = oldServer.net
            ip = IPAddress(net=net, ip=oldServer.ip, device=obj)
            ip.save()
            print(i)
        return {
            'state': True,
            'msg': f'同步成功'
        }

    @button(type='danger', short_description='数据迁移', enable=True, confirm="您确定要生成吗？")
    def migrate(self, request, queryset: QuerySet):
        qss = queryset.all()
        for obj in qss:
            server: ServerNew = obj
            system = None
            if not server.systems.exists():
                system = OperationSystem()
                if server.system == "WindowsServer2016":
                    system_image = OperationSystemImage.objects.filter(name="Windows", version="Server2016").first()
                elif server.system == "CentOS7":
                    system_image = OperationSystemImage.objects.filter(name="CentOS", version="7").first()
                elif server.system == "Ubuntu":
                    system_image = OperationSystemImage.objects.filter(name="Ubuntu", version="18").first()
                else:
                    system_image = None
                system.image = system_image
                system.server = server
                system.rootUsername = server.rootUsername
                system.rootPassword = server.rootPassword
                system.save()
        return {
            'state': True,
            'msg': f'迁移完成'
        }

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
            'min_width': '98px',
            'align': 'center'
        },
        'createdAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'deletedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'ip': {
            'min_width': '200px',
            'align': 'center'
        },
        'net': {
            'min_width': '180px',
            'align': 'center'
        },
        'system': {
            'min_width': '160px',
            'align': 'center'
        },
        'rootPassword': {
            'min_width': '180px',
            'align': 'center'
        },
        'ssh': {
            'min_width': '120px',
            'align': 'center'
        },
        'hoster': {
            'min_width': '320px',
            'align': 'left'
        },
        'group': {
            'min_width': '220px',
            'align': 'left'
        },
        'status': {
            'min_width': '200px',
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


@admin.register(ServerCabinet)
class ServerCabinetAdmin(BaseAdmin):
    list_display = ['code', 'room', "updatedAt", "createdAt", "deletedAt", "id"]
    list_filter = ['room']
    date_hierarchy = 'updatedAt'
    search_fields = ['code', 'room']
    search_help_text = ['你好，这是搜索帮助语句！']
    autocomplete_fields = []
    list_per_page = 10
    fields = ['code', 'room', 'info']
    actions = ['sync']
    inlines = []

    # inlines = [ServerUserInlineAdmin]
    @button(type='danger', short_description='新旧数据同步', enable=True, confirm="您确定要生成吗？")
    def sync(self, request, queryset):
        iService = None
        for i, oldServer in enumerate(Server.objects.all()):
            # net = Net.objects.get_or_create(content=)
            obj = ServerNew(
                id=oldServer.id,
                code=oldServer.code,
                rootUsername=oldServer.rootUsername,
                rootPassword=oldServer.rootPassword,
                hoster=oldServer.hoster,
                system=oldServer.system,
                status=oldServer.status,
                bios=oldServer.bios,
                ssh=oldServer.ssh,
                mac=oldServer.mac,
                remark=oldServer.remark
            )
            obj.save()
            net = oldServer.net
            ip = IPAddress(net=net, ip=oldServer.ip, device=obj)
            ip.save()
            print(i)
        return {
            'state': True,
            'msg': f'同步成功'
        }

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
        'id': {
            'min_width': '88px',
            'align': 'center'
        },
        'code': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'createdAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'deletedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'ip': {
            'min_width': '200px',
            'align': 'center'
        },
        'net': {
            'min_width': '180px',
            'align': 'center'
        },
        'system': {
            'min_width': '160px',
            'align': 'center'
        },
        'rootPassword': {
            'min_width': '180px',
            'align': 'center'
        },
        'ssh': {
            'min_width': '120px',
            'align': 'center'
        },
        'hoster': {
            'min_width': '320px',
            'align': 'left'
        },
        'group': {
            'min_width': '220px',
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
        }
    }


@admin.register(ServerRoom)
class ServerRoomAdmin(BaseAdmin):
    list_display = ['code', "updatedAt", "createdAt", "deletedAt", "id"]
    list_filter = []
    date_hierarchy = 'updatedAt'
    search_fields = ['code']
    search_help_text = ['你好，这是搜索帮助语句！']
    autocomplete_fields = []
    list_per_page = 10
    fields = ['code', 'info']
    actions = ['sync']
    inlines = []

    # inlines = [ServerUserInlineAdmin]
    @button(type='danger', short_description='新旧数据同步', enable=True, confirm="您确定要生成吗？")
    def sync(self, request, queryset):
        iService = None
        for i, oldServer in enumerate(Server.objects.all()):
            # net = Net.objects.get_or_create(content=)
            obj = ServerNew(
                id=oldServer.id,
                code=oldServer.code,
                rootUsername=oldServer.rootUsername,
                rootPassword=oldServer.rootPassword,
                hoster=oldServer.hoster,
                system=oldServer.system,
                status=oldServer.status,
                bios=oldServer.bios,
                ssh=oldServer.ssh,
                mac=oldServer.mac,
                remark=oldServer.remark
            )
            obj.save()
            net = oldServer.net
            ip = IPAddress(net=net, ip=oldServer.ip, device=obj)
            ip.save()
            print(i)
        return {
            'state': True,
            'msg': f'同步成功'
        }

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
        'id': {
            'min_width': '88px',
            'align': 'center'
        },
        'code': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'createdAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'deletedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'ip': {
            'min_width': '200px',
            'align': 'center'
        },
        'net': {
            'min_width': '180px',
            'align': 'center'
        },
        'system': {
            'min_width': '160px',
            'align': 'center'
        },
        'rootPassword': {
            'min_width': '180px',
            'align': 'center'
        },
        'ssh': {
            'min_width': '120px',
            'align': 'center'
        },
        'hoster': {
            'min_width': '320px',
            'align': 'left'
        },
        'group': {
            'min_width': '220px',
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
        }
    }
