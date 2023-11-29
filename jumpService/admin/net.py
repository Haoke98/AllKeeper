# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/27
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin
from django.forms import ModelForm

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


@admin.register(Net)
class NetAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'remark', 'createdAt', 'updatedAt', 'deletedAt']
    search_fields = ['content', 'remark']
    inlines = [IPAddressInlineAdmin]


@admin.register(NetDevice)
class NetDeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'remark', 'mac', 'createdAt', 'updatedAt', 'deletedAt']
    search_fields = ['status', 'remark', 'net', 'mac']
    inlines = [IPAddressInlineAdmin]


@admin.register(IPAddress)
class IPAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'net', 'ip', 'device', 'createdAt', 'updatedAt', 'deletedAt']
    search_fields = ['net', 'ip', 'device']
