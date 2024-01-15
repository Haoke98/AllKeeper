# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/26
@Software: PyCharm
@disc:
======================================="""

from rest_framework import serializers

from ..models import ServerNew


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerNew
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
