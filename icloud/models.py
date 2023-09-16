# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/8/16
@Software: PyCharm
@disc:
======================================="""
import os.path

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

    query_fieldName = models.CharField(max_length=50, null=True, verbose_name="过滤字段")
    query_comparator = models.CharField(max_length=50, null=True, verbose_name="过滤操作")
    query_fieldValue_type = models.CharField(max_length=50, null=True, verbose_name="过滤值数据类型")
    query_fieldValue_value = models.CharField(max_length=50, null=True, verbose_name="过滤值")

    def set_query(self, qs):
        """
        解析相册的QueryFilter信息
        None
        [{'fieldName': 'smartAlbum', 'comparator': 'EQUALS', 'fieldValue': {'type': 'STRING', 'value': 'VIDEO'}}]
        [{'fieldName': 'smartAlbum', 'comparator': 'EQUALS', 'fieldValue': {'type': 'STRING', 'value': 'SLOMO'}}]
        [{'fieldName': 'smartAlbum', 'comparator': 'EQUALS', 'fieldValue': {'type': 'STRING', 'value': 'FAVORITE'}}]
        [{'fieldName': 'parentId', 'comparator': 'EQUALS', 'fieldValue': {'type': 'STRING', 'value': 'D5167F7B-F0A6-4957-B2AC-6523F47CEE7B'}}]

        :param qs:
        :return:
        """
        if qs:
            if len(qs) > 1:
                raise Exception(f"相册[{self.name}]出现了多个QueryFilter信息")
            else:
                q = qs[0]
                self.query_fieldName = q['fieldName']
                self.query_comparator = q['comparator']
                fieldValue = q['fieldValue']
                self.query_fieldValue_type = fieldValue['type']
                self.query_fieldValue_value = fieldValue['value']

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


def upload(instance, filename, dst_dir):
    # 获取对象的ID
    fn = instance.id.replace("/", "-")
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    # 返回新的文件路径，格式为 "ID.ext"
    fne = f"{fn}.{ext}"
    _dir = os.path.join("LocalMedia", dst_dir)
    fp = os.path.join(_dir, fne)
    return fp


def upload_thumb(instance, filename):
    return upload(instance, filename, "thumb")


def upload_prv(instance, filename):
    return upload(instance, filename, "prv")


def upload_origin(instance, filename):
    return upload(instance, filename, "origin")


class IMedia(BaseModel):
    id = models.CharField(max_length=50, primary_key=True)
    filename = models.CharField(max_length=100, verbose_name="文件名", null=True)
    ext = models.CharField(max_length=10, verbose_name="扩展名")
    size = models.BigIntegerField(verbose_name="大小", null=True)
    dimensionX = models.IntegerField(verbose_name="DX", null=True)
    dimensionY = models.IntegerField(verbose_name="DY", null=True)
    asset_date = models.DateTimeField(verbose_name="生成时间", null=True)
    added_date = models.DateTimeField(verbose_name="加入icloud的时间", null=True)
    versions = models.TextField(null=True)
    albums = fields.ManyToManyField(to=Album, verbose_name="相册")
    startRank = models.IntegerField(null=True)
    thumbURL = models.TextField(null=True)

    isHidden = models.BooleanField(null=True, verbose_name="隐藏")
    isFavorite = models.BooleanField(null=True, verbose_name="收藏")
    deleted = models.BooleanField(null=True, verbose_name="已删除")

    createdDeviceID = models.CharField(max_length=255, verbose_name="创建的设备ID", null=True)
    createdUserRecordName = models.CharField(max_length=255, null=True, verbose_name="创建的用户ID")
    modifiedDeviceID = models.CharField(max_length=255, verbose_name="更新的设备ID", null=True)
    modifiedUserRecordName = models.CharField(max_length=255, verbose_name="更新的用户ID", null=True)

    duration = models.PositiveIntegerField(null=True, verbose_name="时长")
    adjustmentRenderType = models.IntegerField(null=True)
    timeZoneOffset = models.IntegerField(null=True)
    burstFlags = models.IntegerField(null=True)
    # orientationOpts = ((0, '横向'), (1, "纵向"))
    orientation = models.IntegerField(null=True, verbose_name="方向")

    locationEnc = models.TextField(null=True, verbose_name="地址信息(已加密)")

    masterRecordChangeTag = models.CharField(max_length=50, null=True)
    assetRecordChangeTag = models.CharField(max_length=50, null=True)

    masterRecordType = models.CharField(max_length=50, null=True)
    assetRecordType = models.CharField(max_length=50, null=True)

    masterRecord = models.TextField(null=True)
    assetRecord = models.TextField(null=True)

    class Meta:
        verbose_name = "iCloud媒体"
        ordering = ('-asset_date',)


class LocalMedia(BaseModel):
    id = models.CharField(max_length=50, primary_key=True)

    filename = models.CharField(max_length=100, verbose_name="文件名", null=True)
    ext = models.CharField(max_length=10, verbose_name="扩展名", null=True)
    size = models.BigIntegerField(verbose_name="大小", null=True)
    duration = models.PositiveIntegerField(null=True, verbose_name="时长")
    dimensionX = models.IntegerField(verbose_name="DX", null=True)
    dimensionY = models.IntegerField(verbose_name="DY", null=True)
    orientation = models.IntegerField(null=True, verbose_name="方向")
    adjustmentRenderType = models.IntegerField(null=True)
    timeZoneOffset = models.IntegerField(null=True)
    burstFlags = models.IntegerField(null=True)

    masterRecordChangeTag = models.CharField(max_length=50, null=True)
    assetRecordChangeTag = models.CharField(max_length=50, null=True)

    asset_date = models.DateTimeField(verbose_name="生成时间", null=True)
    added_date = models.DateTimeField(verbose_name="加入icloud的时间", null=True)
    detach_icloud_date = models.DateTimeField(verbose_name="从icloud中移除时间", null=True)

    locationEnc = models.TextField(null=True, verbose_name="地址信息(已加密)", blank=True)

    thumb = models.ImageField(verbose_name="缩略图", upload_to=upload_thumb, null=True, help_text="视频和图像都会有，JPEG格式")
    prv = models.FileField(verbose_name="可预览文件", null=True, upload_to=upload_prv,
                           help_text="HICH图片和PNG图片的可预览文件为JPEG图，MOV视频的可预览文件为MP4")
    origin = models.FileField(verbose_name="原始文件", null=True, upload_to=upload_origin)

    versions = models.TextField(null=True)
    masterRecord = models.TextField(null=True)
    assetRecord = models.TextField(null=True)
    assetRecordAfterDelete = models.TextField(null=True)

    class Meta:
        verbose_name = "本地资源"
        ordering = ('-asset_date',)
