# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/27
@Software: PyCharm
@disc:
======================================="""
from django.views.decorators.csrf import csrf_exempt

from utils.http_helper import RestResponse


@csrf_exempt
def login(request):
    username: str = request.POST.get("username")
    password: str = request.POST.get("password")
    return RestResponse(200, "ok", {
        "token": "SCUI.Administrator.Auth",
        "userInfo": {
            "userId": "1",
            "userName": "Administrator",
            "dashboard": "0",
            "role": [
                "SA",
                "admin",
                "Auditor"
            ]
        }
    })
