# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/11/12
@Software: PyCharm
@disc:
======================================="""
import hashlib


def md5(v: str):
    return hashlib.md5(v.encode("utf-8")).hexdigest()


if __name__ == '__main__':
    print(md5("123456"))
