# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/8/16
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from django.db.models import Count, Sum
from simplepro.components import fields

from izBasar.models import BaseModel


class Album(BaseModel):
    name = models.CharField(max_length=50, verbose_name="标题", primary_key=True)
    total = models.PositiveIntegerField(default=0, verbose_name="iCloud上的数量")
    count = models.PositiveIntegerField(default=0, verbose_name="已经采集到的数量")
    synced = models.BooleanField(default=False, verbose_name='同步完毕')
    size = models.PositiveBigIntegerField(default=0, verbose_name="大小")

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.synced = self.count == self.total
        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)

    def agg(self):
        imedia_count = self.imedia_set.aggregate(Count('id'))['id__count']
        total_size = self.imedia_set.aggregate(total=Sum('size'))['total']
        print(f"{self.name}: aggs:[{imedia_count},{total_size}]")
        self.count = imedia_count
        if total_size is not None:
            self.size = total_size
        # if len(photos) == 0 or :

    class Meta:
        verbose_name = "iCloud相册"


class IMedia(BaseModel):
    id = models.CharField(max_length=50, primary_key=True)
    filename = models.CharField(max_length=100, verbose_name="文件名")
    ext = models.CharField(max_length=10, verbose_name="扩展名")
    size = models.BigIntegerField(verbose_name="大小")
    dimensionX = models.IntegerField(verbose_name="DX")
    dimensionY = models.IntegerField(verbose_name="DY")
    asset_date = models.DateTimeField(verbose_name="生成时间")
    added_date = models.DateTimeField(verbose_name="加入icloud的时间")
    versions = models.TextField()
    albums = fields.ManyToManyField(to=Album, verbose_name="相册")

    class Meta:
        verbose_name = "iCloud媒体"
