import logging

import jwt
from django.utils.deprecation import MiddlewareMixin

from proj.secret import JWT_SIGNATURE
from utils.http_helper import RestResponse


class AuthCheck(MiddlewareMixin):
    """
    鉴权中间件
    """

    def process_request(self, request):
        if str(request.path).startswith("/all-keeper/"):
            if request.path != "/all-keeper/login" and request.path != "/all-keeper/breath":
                if str(request.path).startswith("/all-keeper/images/thumbnail"):
                    token = request.GET.get('token')
                else:
                    if not request.headers.keys().__contains__('Authorization'):
                        return RestResponse(1200, "请提供身份认证Token")
                    token = request.headers['Authorization'].replace("Bearer ", "")
                try:
                    payload_data = jwt.decode(token, JWT_SIGNATURE, algorithms=['HS256'])
                    # TODO: 处理payload
                    print("payloadData:", payload_data)
                except jwt.ExpiredSignatureError:
                    return RestResponse(1200, "token 已经失效")
                except Exception as _err:
                    logging.error(f"鉴权异常：[{_err}]")
                    return RestResponse(4200, "token 解析失败")

    def process_response(self, request, response):
        return response
