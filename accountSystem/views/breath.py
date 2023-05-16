# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/5/15
@Software: PyCharm
@disc:
======================================="""
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import BreathInfo


@csrf_exempt
def BreathView(request):
    if request.method == "POST":
        data = json.loads(request.body)
        obj = BreathInfo(accessAt=data["accessAt"], mac=data["mac"], ip=request.META.get('REMOTE_ADDR'),
                         latitude=data["latitude"],
                         longitude=data["longitude"])
        obj.save()
    return HttpResponse("ok")
