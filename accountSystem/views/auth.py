# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/27
@Software: PyCharm
@disc:
======================================="""
import datetime
import json

from django.views.decorators.csrf import csrf_exempt

from proj.secret import ADMIN_USERNAME, ADMIN_PASSWORD, JWT_SIGNATURE, JWT_ISSUER
from proj.settings import JWT_EXPIRED_DELTA
from utils.encrypt import md5
from utils.http_helper import RestResponse

import jwt

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username: str = data.get("username")
        password: str = data.get("password")
        if username == ADMIN_USERNAME and password == md5(ADMIN_PASSWORD):
            payload = {
                'exp': datetime.datetime.utcnow() + JWT_EXPIRED_DELTA,  # 过期时间
                'iat': datetime.datetime.utcnow(),  # 开始时间
                'iss': JWT_ISSUER,  # 签名
                'data': {  # 内容，一般存放该用户id和开始时间
                    'username': username,
                    'b': 2,
                },
            }
            token = jwt.encode(payload, JWT_SIGNATURE, algorithm='HS256')
            return RestResponse(200, "ok", {
                "token": token,
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
        else:
            return RestResponse(502, "username and password is incorrect.")
