import json

from django.http import JsonResponse, HttpResponse

from .models import *


# Create your views here.
def makeJS(request):
    return JsonResponse("xx")


def getMaps(request):
    result = {'err_msg': 'ok', 'objects': []}
    maps = Map.objects.all()
    dict = []
    for map in maps:
        dict.append(map.json())
    result['objects'] = dict
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')
