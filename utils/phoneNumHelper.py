# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/6/14
@Software: PyCharm
@disc:
======================================="""
import re
from urllib.parse import urlencode  # python3

import requests


def get_carrier(phone_number: str) -> str:
    # 使用正则表达式，匹配输入是否是正确的11位手机号
    pattern = re.compile(r'^1[3-9]\d{9}$')
    if pattern.match(phone_number):
        # 中国移动
        china_mobile = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '157', '158', '159', '182',
                        '183', '184', '187', '188', '1705', '178', '147']
        # 中国联通
        china_unicom = ['130', '131', '132', '155', '156', '185', '186', '1709', '176', '145']
        # 中国电信
        china_telecom = ['133', '153', '180', '181', '189', '1700', '177']

        # 获取手机号前三位
        prefix = phone_number[:3]

        if prefix in china_mobile:
            return "中国移动"
        elif prefix in china_unicom:
            return "中国联通"
        elif prefix in china_telecom:
            return "中国电信"
        else:
            return "未知运营商"
    else:
        return "无效的手机号码"


def get_location_carrier_info(token, tel):
    params = urlencode({'mobile': tel, 'datatype': 'json'})
    url = 'https://api.ip138.com/mobile/?' + params
    headers = {"token": token}  # token为示例
    resp = requests.get(url, 'GET', headers=headers)
    return resp.text.split(" ")


if __name__ == '__main__':
    get_location_carrier_info("d2d4f78056097718ea20fb835b9b2251", "17590037828")
