# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/26
@Software: PyCharm
@disc:
======================================="""

# Create your views here.
import datetime as dt
import json
import os
import uuid

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .auth import login
from .device import DeviceView, DeviceRegionView
from .human import HumanView, HumanViewSet
from .menu import getMenuList


@csrf_exempt
def upload_image(request, dir_name):
    result = {"error": 1, "message": "上传出错"}
    files = request.FILES.get("imgFile", None)
    if files:
        result = image_upload(files, dir_name)
    return HttpResponse(json.dumps(result), content_type="application/json")


# 目录创建
def upload_generation_dir(dir_name):
    today = dt.datetime.today()
    dir_name = dir_name + '/%d/%d/' % (today.year, today.month)
    if not os.path.exists(settings.MEDIA_ROOT + dir_name):
        os.makedirs(settings.MEDIA_ROOT + dir_name)
    return dir_name


# 图片上传
def image_upload(files, dir_name):
    # 允许上传文件类型
    allow_suffix = ['jpg', 'png', 'jpeg', 'gif',
                    'bmp', 'zip', "swf", "flv",
                    "mp3", "wav", "wma", "wmv",
                    "mid", "avi", "mpg", "asf",
                    "rm", "rmvb", "doc", "docx",
                    "xls", "xlsx", "ppt", "htm",
                    "html", "txt", "zip", "rar",
                    "gz", "bz2"]
    file_suffix = files.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "图片格式不正确"}
    relative_path_file = upload_generation_dir(dir_name)
    path = os.path.join(settings.MEDIA_ROOT, relative_path_file)
    if not os.path.exists(path):  # 如果目录不存在创建目录
        os.makedirs(path)
    file_name = str(uuid.uuid1()) + "." + file_suffix
    path_file = os.path.join(path, file_name)
    file_url = settings.MEDIA_URL + relative_path_file + file_name
    open(path_file, 'wb').write(files.file.read())
    return {"error": 0, "url": file_url}
