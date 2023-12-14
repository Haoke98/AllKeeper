from django.contrib import admin
from simplepro.decorators import button

from izBasar.admin import BaseAdmin
from .net import IPAddressInlineAdmin
from ..models import Server, ServerNew, IPAddress, ServerCabinet, ServerRoom


@admin.register(Server)
class ServerAdmin(BaseAdmin):
    list_display = ['code', 'net', "ip", 'system', 'rootPassword', 'ssh', 'status', 'remark', 'bios', 'hoster',
                    "updatedAt",
                    "createdAt",
                    "deletedAt", ]
    list_display_links = ['remark', 'hoster']
    list_filter = ['hoster', 'ssh', 'system', 'net', 'status']
    date_hierarchy = 'updatedAt'
    search_fields = ['ip', 'remark', 'code']
    search_help_text = ['你好，这是搜索帮助语句！']
    autocomplete_fields = ['net']
    list_per_page = 10
    fields = ['code', 'hoster', 'net', 'ip', 'system', 'rootUsername', 'rootPassword', 'status', 'bios', 'ssh',
              'mac',
              'remark',
              'info']

    # inlines = [ServerUserInlineAdmin]

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
            'fixed': 'left',
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


@admin.register(ServerNew)
class ServerNewAdmin(BaseAdmin):
    list_display = ['code', 'ssh', 'system', 'status', 'bios', 'cabinet', 'remark', 'hoster',
                    "mac", "updatedAt", "createdAt", "deletedAt", "id"
                    ]
    list_display_links = ['remark', 'hoster']
    list_filter = ['hoster', 'ssh', 'status', 'cabinet__room', 'cabinet']
    date_hierarchy = 'updatedAt'
    search_fields = ['remark', 'code']
    search_help_text = ['你好，这是搜索帮助语句！']
    autocomplete_fields = []
    list_per_page = 10
    fields = ['code', 'cabinet', 'hoster', 'status', 'bios', 'mac', 'remark', 'info']
    actions = ['sync']
    inlines = [IPAddressInlineAdmin]

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
