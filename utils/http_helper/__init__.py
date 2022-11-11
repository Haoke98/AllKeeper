# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/26
@Software: PyCharm
@disc:
======================================="""
import json

from django.http import HttpResponse


class RestResponse(HttpResponse):
    code: int = 200
    msg: str = "ok"
    data: any = None

    def __init__(self, code, msg, data=None, serialize: bool = True):
        self.code = code
        self.msg = msg
        if data is None:
            content = f'{{"code":{code},"message":"{msg}"}}'
        else:
            if serialize:
                if type(data) is dict:
                    data = json.dumps(data, ensure_ascii=False)
                else:
                    from django.core import serializers
                    data = serializers.serialize('json', data)

            content = f'{{"code":{code},"message":"{msg}","data":{data} }}'
        super(RestResponse, self).__init__(content, content_type="application/json")
