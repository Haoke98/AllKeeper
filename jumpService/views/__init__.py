# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/15
@Software: PyCharm
@disc:
======================================="""
import datetime
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .server import ServerViewSet


@csrf_exempt
def collect(request, *args, **kwargs):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(datetime.datetime, "接受了数据:", data)
        return HttpResponse("ok")
