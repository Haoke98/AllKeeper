# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/7/6
@Software: PyCharm
@disc:
======================================="""
import base64
from urllib.parse import urlparse

import requests


def is_url(string):
    parsed_url = urlparse(string)
    return bool(parsed_url.scheme)


def image_to_base64(url_or_path):
    if is_url(url_or_path):
        response = requests.get(url_or_path)
        encoded_string = base64.b64encode(response.content)
        return encoded_string.decode('utf-8')
    else:
        with open(url_or_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return encoded_string.decode('utf-8')
