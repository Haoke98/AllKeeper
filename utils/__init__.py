# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/25
@Software: PyCharm
@disc:
======================================="""
import decimal
import math


def human_readable_bytes(num_bytes):
    if num_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(num_bytes, 1024)))
    p = math.pow(1024, i)
    p_decimal = decimal.Decimal(p)
    s = round(num_bytes / p_decimal, 2)
    return "%s %s" % (s, size_name[i])


def human_readable_time(milliseconds):
    seconds = milliseconds // 1000
    minutes = seconds // 60
    hours = minutes // 60

    if hours > 0:
        return f"{hours}小时 {minutes % 60}分钟 {seconds % 60}秒 {milliseconds % 1000}毫秒"
    elif minutes > 0:
        return f"{minutes}分钟 {seconds % 60}秒 {milliseconds % 1000}毫秒"
    elif seconds > 0:
        return f"{seconds}秒 {milliseconds % 1000}毫秒"
    else:
        return f"{milliseconds}毫秒"
