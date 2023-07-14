# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/7/13
@Software: PyCharm
@disc:
======================================="""
from .models import Weibo


def weibo_collect():
    print("采集数据中:", )
    Weibo.objects.filter()
    total = 0
    for id in range(ab[0], ab[1]):
        obj = Weibo(id=id)
        if obj.collect():
            obj.save()
            print(f"采集了微博账户[{obj.id}]")
            total += 1
        else:
            print(f"微博账户[{id}]不存在或者存在异常")
    print("本次总共采集了", total, "个账户数据")