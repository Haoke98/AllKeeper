import os
from datetime import datetime

import requests
from django.shortcuts import redirect

from izBasar.settings import IMAGE_ROOT
from miniProgram.models.image import Image


def proxy(request):
    id = request.GET.get("id")
    imageObj = Image.objects.get(id=id)
    print(imageObj.content.path)
    p = os.path.join(IMAGE_ROOT, imageObj.file_name)
    if os.path.exists(p):
        print("已存在")
    else:
        print("重新加载")
        resp = requests.get(imageObj.original_url)
        imageObj.file_name = "%s%s" % (str(datetime.now().microsecond), ".jpg")
        tempFilePath = os.path.join(IMAGE_ROOT, imageObj.file_name)
        with open(tempFilePath, 'wb') as f:
            f.write(resp.content)
        imageObj.save()
    return redirect(to="/media/img/" + imageObj.file_name)
