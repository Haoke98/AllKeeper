# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/10/31
@Software: PyCharm
@disc:
======================================="""
from rest_framework import serializers

from .models import IMedia, LocalMedia


class IMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IMedia
        fields = '__all__'


class LocalMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalMedia
        fields = '__all__'
