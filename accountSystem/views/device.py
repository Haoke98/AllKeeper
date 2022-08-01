# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/28
@Software: PyCharm
@disc:
======================================="""
from rest_framework import viewsets

from ..models import Device
from ..pagination import StandardPagination
from ..serializers import DeviceSerializer


class DeviceViewSets(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    pagination_class = StandardPagination
