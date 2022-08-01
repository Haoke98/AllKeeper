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


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'id',
            'createdAt',
            'updatedAt',
            'deletedAt',
            'ip',
            'port',
            'country',
            'subDivision',
            'city',
            'isp',
            'asn',
            'org',
            'product',
            'service',
            'usersXmlOk',
            'confOk',
            'snapshotOk'
        )
