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

from izBasar.secret import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.encrypt import md5
from utils.http_helper import RestResponse

from jwcrypto import jwt, jwk

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username: str = data.get("username")
        password: str = data.get("password")
        if username == ADMIN_USERNAME and password == md5(ADMIN_PASSWORD):
            key = jwk.JWK(generate='oct', size=256)
            token = jwt.JWT(header={"alg": "HS256"}, claims={"username": username, "createdAt": str(datetime.datetime.now())})
            token.make_signed_token(key)
            jwt_str = token.serialize()
            return RestResponse(200, "ok", {
                "token": jwt_str,
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
