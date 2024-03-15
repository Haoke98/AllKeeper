# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/14
@Software: PyCharm
@disc:
======================================="""
from simplepro.models import BaseModel
from simplepro.components import fields


class Brand(BaseModel):
    name = fields.CharField(max_length=100)
