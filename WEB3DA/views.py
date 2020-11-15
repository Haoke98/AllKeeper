import json

from django.http import JsonResponse, HttpResponse

from .models import *


# Create your views here.
def makeJS(request):
    return JsonResponse("xx")


def getMaps(request):
    """
    this API is build for the Project:WEB3DAnimation.
    :param request: this is a UWSGI requests.
    :return: JSON object that collected the url of the maps on server.
    """
    # print(x)
    # send_mail('getMaps(request):', 'Here is the message: the django has been pri', '1903249375@qq.com',
    #           ['kws11@qq.com', '1903249375@qq.com'], fail_silently=False)
    result = {'err_msg': 'ok', 'objects': []}
    maps = Map.objects.all()
    dict = []
    for map in maps:
        dict.append(map.json())
    result['objects'] = dict
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')
