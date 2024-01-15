# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/15
@Software: PyCharm
@disc:
======================================="""
import json
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .server import ServerViewSet
from ..models import ServerStatus


@csrf_exempt
def collect(request, *args, **kwargs):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        authorization = request.headers.get('Authorization')
        key = authorization.replace('Bearer ', '')
        logging.info(f"key: {key}, 数据:{data}")
        st = ServerStatus(server_id=key, cpuUsage=data['cpu_usage'], memoryUsage=data['memory_usage'],
                          diskUsage=data['disk_usage'])
        st.save()
        return HttpResponse("ok")
