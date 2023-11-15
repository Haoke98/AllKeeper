# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/28
@Software: PyCharm
@disc:
======================================="""
from rest_framework import serializers

from ..models import Device


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'id',
            'createdAt',
            'updatedAt',
            'deletedAt',
            'group',
            'ip',
            'rootUsername',
            'rootPassword',
            'hoster',
            'bios',
            'remark'
        )
