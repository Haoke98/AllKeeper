# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/27
@Software: PyCharm
@disc:
======================================="""
import ipaddress

from simplepro.components import fields
from simplepro.models import BaseModel


class Net(BaseModel):
    content = fields.CharField(max_length=18, verbose_name="CIDR")
    netmask = fields.CharField(max_length=15, verbose_name="子网俺码", default="255.255.255.0")
    remark = fields.CharField(verbose_name="备注", max_length=100, null=True, blank=True)

    def _class(self):
        res = ""
        head = self.content.split(".")[0]
        if int(head) in range(1, 127):
            res = "A"
        elif int(head) in range(128, 192):
            res = "B"
        elif int(head) in range(192, 224):
            res = "C"
        else:
            print(f"无效网络地址:[{self.content}]")
            pass
        return res

    _class.short_description = "类型"

    def is_global(self):
        network = ipaddress.IPv4Network(self.content)
        return network.is_global

    is_global.short_description = "公网/私网"

    def address_count(self):
        network = ipaddress.IPv4Network(self.content)
        return network.num_addresses

    address_count.short_description = "地址数量"

    def broadcast_address(self):
        network = ipaddress.IPv4Network(self.content)
        return network.broadcast_address

    broadcast_address.short_description = "广播地址"

    def __str__(self):
        if self.remark:
            return "{} ({})".format(self.content, self.remark)
        return self.content

    class Meta:
        verbose_name = "网段"
        verbose_name_plural = verbose_name
        ordering = ('-updatedAt',)
