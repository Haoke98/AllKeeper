# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/11/5
@Software: PyCharm
@disc:
======================================="""
from rest_framework import serializers

from ..models import Human


class HumanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Human
        fields = (
            'id',
            'createdAt',
            'updatedAt',
            'deletedAt',
            'name'
        )
