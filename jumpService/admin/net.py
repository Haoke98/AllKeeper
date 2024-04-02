# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/27
@Software: PyCharm
@disc:
======================================="""
import ipaddress

from django.contrib import admin
from django.db.models import QuerySet
from django.forms import ModelForm
from simplepro.admin import FieldOptions, BaseAdmin
from simplepro.components.fields.char_field import CharFormField

from ..models import Net, IPAddress, NetDevice


class IPAddressForm(ModelForm):
    class Meta:
        model = IPAddress
        fields = ['device', 'net', 'ip']


class IPAddressInlineAdmin(admin.TabularInline):
    model = IPAddress
    form = IPAddressForm
    min_num = 0
    extra = 0


class NetWorkForm(ModelForm):
    ip = CharFormField(required=False)

    class Meta:
        model = Net
        fields = ['remark', 'netmask']


class NetFilter(admin.SimpleListFilter):
    title = '公网/私网'
    parameter_name = 'is_global'

    def lookups(self, request, model_admin):
        return (
            ('global', '公网'),
            ('private', '私网')
        )

    def queryset(self, request, queryset: QuerySet):
        _private = []
        _global = []
        qss = queryset.filter().all()
        for qs in qss:
            network = ipaddress.IPv4Network(qs.content)
            if network.is_global:
                _global.append(qs.id)
            else:
                _private.append(qs.id)
        qs = None
        if self.value() == 'global':
            qs = queryset.filter(id__in=_global)
        elif self.value() == 'private':
            qs = queryset.filter(id__in=_private)
        else:
            qs = queryset
        return qs


@admin.register(Net)
class NetWorkAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'netmask', 'is_global', '_class', 'address_count', 'remark', 'broadcast_address',
                    'createdAt', 'updatedAt',
                    'deletedAt']
    list_filter = ('netmask', NetFilter)
    search_fields = ['content', 'remark']
    form = NetWorkForm
    inlines = [IPAddressInlineAdmin]

    def save_model(self, request, obj, form, change):
        # 计算网段的 CIDR 表示
        if 'ip' in form.changed_data or 'netmask' in form.changed_data:
            ip_net = ipaddress.ip_network((form.cleaned_data['ip'], form.cleaned_data['netmask']), strict=False)
            obj.content = str(ip_net)
            obj.isGlobal = ip_net.is_global

        # 父级 save_model 方法将调用 save 方法来保存修改后的对象
        super(NetWorkAdmin, self).save_model(request, obj, form, change)

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
        'deletedAt': {
            'width': '180px',
            'align': 'left'
        },
        'content': {
            'width': '180px',
            'align': 'left'
        },
        'is_global': {
            'width': '120px',
            'align': 'center'
        },
        'netmask': {
            'width': '160px',
            'align': 'left'
        },
        'broadcast_address': {
            'width': '160px',
            'align': 'left'
        },
        'apmPwd': {
            'width': '200px',
            'align': 'left'
        },
        'logstashPwd': {
            'width': '200px',
            'align': 'left'
        },
        'beatsPwd': {
            'width': '200px',
            'align': 'left'
        },
        'remark': {
            'width': '240px',
            'align': 'left'
        }
    }


@admin.register(NetDevice)
class NetDeviceAdmin(BaseAdmin):
    list_display = ['id', 'remark', 'mac', 'createdAt', 'updatedAt', 'deletedAt']
    search_fields = ['status', 'remark', 'net', 'mac']
    ordering = ('-updatedAt',)
    inlines = [IPAddressInlineAdmin]
    fields_options = {
        'id': FieldOptions.UUID,
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'remark': FieldOptions.REMARK,
        'status': FieldOptions.REMARK,
        'mac': FieldOptions.MAC_ADDRESS
    }


@admin.register(IPAddress)
class IPAddressAdmin(BaseAdmin):
    list_display = ['id', 'net', 'ip', 'device', 'createdAt', 'updatedAt', 'deletedAt']
    search_fields = ['net', 'ip', 'device']
    ordering = ('-updatedAt', '-createdAt')
    fields_options = {
        'id': FieldOptions.UUID,
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'net': {
            'min_width': "280px",
            'align': 'left',
            "resizeable": True,
            "show_overflow_tooltip": True
        },
        'ip': FieldOptions.IP_ADDRESS,
        'device': {
            'min_width': '400px',
            'align': 'left',
            "resizeable": True,
            "show_overflow_tooltip": True
        },
        'broadcast_address': {
            'width': '220px',
            'align': 'left'
        },
        'apmPwd': {
            'width': '200px',
            'align': 'left'
        },
        'logstashPwd': {
            'width': '200px',
            'align': 'left'
        },
        'beatsPwd': {
            'width': '200px',
            'align': 'left'
        },
        'remark': FieldOptions.REMARK
    }
