# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/27
@Software: PyCharm
@disc:
======================================="""
from simplepro.components import fields
from simplepro.models import BaseModel


class Net(BaseModel):
    content = fields.CharField(max_length=15)
    remark = fields.CharField(verbose_name="备注", max_length=100)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "网段"
        verbose_name_plural = verbose_name


