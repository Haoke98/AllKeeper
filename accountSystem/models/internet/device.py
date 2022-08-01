# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/28
@Software: PyCharm
@disc:
======================================="""
from django.db import models

from izBasar.models import BaseModel
from .isp import Isp
from ..region import Country, SubDivision, City


class Device(BaseModel):
    ip = models.GenericIPAddressField(null=False, blank=False, unique=True)
    port = models.IntegerField(default=80)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, null=True)
    subDivision = models.ForeignKey(to=SubDivision, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, null=True)
    isp = models.ForeignKey(to=Isp, on_delete=models.CASCADE, null=True)
    asn = models.IntegerField(blank=True, null=True)
    org = models.CharField(max_length=50, blank=True, null=True)
    product = models.CharField(max_length=50, blank=True, null=True)
    service = models.CharField(max_length=50, blank=True, null=True)
    usersXmlOk = models.BooleanField(default=False, null=True)
    usersXml = models.TextField(null=True)
    confOk = models.BooleanField(default=False, null=True)
    conf = models.TextField(null=True)
    snapshotOk = models.BooleanField(default=False, null=True)
