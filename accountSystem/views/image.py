import base64
import math
import os
from io import BytesIO

from PIL import Image
from django.http import HttpResponse

from utils.http_helper import RestResponse


def thumbnail(request):
    import pyheif
    if request.method == 'GET':
        image_path: str = request.GET.get('path')
        image_path = image_path.replace(' ', '+')
        if image_path.endswith(".heic") or image_path.endswith(".HEIC"):
            hief_img = pyheif.read(image_path)
            image = Image.frombytes(hief_img.mode, hief_img.size, hief_img.data, "raw", hief_img.mode, hief_img.stride)
        else:
            image = Image.open(image_path)
        width = int(request.GET.get("width", 200))
        height = int(request.GET.get("height", 200))
        image.thumbnail((width, height))
        image = image.convert('RGB')
        # output_buffer = BytesIO()
        # image.save(output_buffer, 'JPEG')
        # byte_data = output_buffer.getvalue()
        # base64_str = base64.b64encode(byte_data).decode('utf-8')
        # return RestResponse(200, "ok", {'base64_str':base64_str})
        resp = HttpResponse(content_type="image/jpeg")
        image.save(resp, 'JPEG')
        return resp


def image_view(request):
    PHOTOS_DIR = "/external/SADAM/icloud/photos"
    if request.method == 'GET':
        p = int(request.GET.get('page', 1))
        ps = int(request.GET.get('pageSize', 20))
        img_list = os.listdir(PHOTOS_DIR)
        for img in img_list:
            if img.startswith('._'):
                img_list.remove(img)
        rows = img_list[(p - 1) * ps:p * ps]
        return RestResponse(200, "ok", {
            "total": len(img_list),
            "totalPage": math.ceil(len(img_list) / 10),
            "rows": [{
                "key": index,
                "fileName": item,
                "path": os.path.join(PHOTOS_DIR, item)
            } for index, item in enumerate(rows)]
        })
