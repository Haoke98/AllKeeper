# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/9/14
@Software: PyCharm
@disc:
======================================="""
import datetime
import json
import logging
import math
import os
import threading
import time
import traceback

from . import iService
from .models import IMedia


def insert_or_update_media(startRank: int, p):
    fn, ext = os.path.splitext(p.filename)
    ext = str(ext).upper()
    startedAt1 = time.time()
    obj, created = IMedia.objects.get_or_create(id=p.id)
    print(f"查询[{obj.id}]成功！[Created:{created},Duration:{time.time() - startedAt1} s]")
    startedAt2 = time.time()
    if created:
        obj.filename = p.filename
        obj.ext = ext
        obj.size = p.size
        obj.dimensionX = p.dimensions[0]
        obj.dimensionY = p.dimensions[1]
        obj.asset_date = p.asset_date
        obj.added_date = p.added_date
        # download_thumb(obj, p)
        # download_prv(obj, p)
    obj.startRank = startRank  # 每次startRank都会变
    obj.versions = json.dumps(p.versions, indent=4, ensure_ascii=False)
    fields: dict = p._master_record['fields']
    if fields.keys().__contains__("resJPEGThumbRes"):
        obj.thumbURL = fields['resJPEGThumbRes']['value']['downloadURL']
    else:
        obj.thumbURL = fields['resOriginalRes']['value']['downloadURL']
    #     try:
    #         if obj.thumb or not os.path.exists(obj.thumb.path):
    #             download_thumb(obj, p)
    #     except ValueError as e:
    #         if "The 'thumb' attribute has no file associated with it." in str(e):
    #             download_thumb(obj, p)
    #         else:
    #             raise ValueError(e)
    #     try:
    #         if obj.prv or not os.path.exists(obj.prv.path):
    #             download_prv(obj, p)
    #     except ValueError as e:
    #         if "The 'prv' attribute has no file associated with it." in str(e):
    #             download_prv(obj, p)
    #         else:
    #             raise ValueError(e)
    print(f"预处理[{obj.id}]成功！[Duration:{time.time() - startedAt2} s]")
    startedAt3 = time.time()
    obj.save()
    print(f"保存[{obj.id}]成功！[Duration:{time.time() - startedAt3} s]")
    return obj


def update(records, startRank):
    def do(_records, _startRank):
        iPhotos = iService.record2iphoto(_records)
        for i, iphoto in enumerate(iPhotos):
            insert_or_update_media(_startRank + i, iphoto)

    th = threading.Thread(target=do, args=(records, startRank))
    th.start()


def collect(startRank: int, _id):
    resp = iService.query_medias(startRank=startRank)
    records: list[dict] = resp['records']
    update(records, startRank)


STATUS_FINISHED = "FINISHED"
STATUS_STOP = "STOPPING"
STATUS_RUNNING = "Running"
STATUS_EXCEPTION = "Exception"
STATUS = STATUS_STOP

TOTAL = -1
FINISHED_COUNT = 0
STARTED_AT = datetime.datetime.now()
EXCEPTION_MSG = None
EXCEPTION_TRACE_BACK = None


def collect_all_medias():
    global STATUS, FINISHED_COUNT, TOTAL, STARTED_AT, EXCEPTION_MSG, EXCEPTION_TRACE_BACK
    # for album in albums:
    #     photos = iService.photos.albums[album.name]
    #     total = len(photos)
    # if album.count == total:
    #     print(f"{album.name}: 无需同步跳过")
    #     continue
    # for i, p in enumerate(photos):
    #     th = threading.Thread(target=collect, args=(p, album, i, total))
    #     th.start()
    # album.agg()
    # album.save()
    # target_photo = None
    STATUS = STATUS_RUNNING
    STARTED_AT = datetime.datetime.now()
    try:
        _, TOTAL = iService.media_total()
        medias = iService.photos.all
        FINISHED_COUNT = 0
        for i, photo in enumerate(medias):
            FINISHED_COUNT = i + 1
            progress = FINISHED_COUNT / TOTAL * 100
            dlt = datetime.datetime.now() - STARTED_AT
            finishedCount = math.ceil(TOTAL * progress / 100)
            speed_in_second = finishedCount / dlt.total_seconds()
            left = TOTAL - finishedCount
            dlt_in_second = left / speed_in_second
            dlt1 = datetime.timedelta(seconds=dlt_in_second)
            willFinishedAt = datetime.datetime.now() + dlt1
            startedAt = time.time()
            insert_or_update_media(i, photo)
            print(f"{progress:.2f}% ({FINISHED_COUNT}/{TOTAL}), {photo}, [Duration:{time.time() - startedAt} s]")
        STATUS = STATUS_FINISHED
    except Exception as e:
        STATUS = STATUS_EXCEPTION
        EXCEPTION_MSG = str(e)
        EXCEPTION_TRACE_BACK = traceback.format_exc()
        logging.error("iCloud数据同步异常", exc_info=True)
