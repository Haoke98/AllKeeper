import json
import requests

from django.http import HttpResponse

# from django.http import request
from .models import *


# Create your views here.
def getSlider(request):
    result = {'err_msg': "OK", 'objects': []}
    app = settings.objects.first()
    sliders = app.sliders.all()
    dicts = []
    for per in sliders:
        video_dic = {'name': per.name,
                     'cover': per.cover, 'url': per.url, 'id': per.id, 'film_id': per.belongTo.id}
        dicts.append(video_dic)
    result['objects'] = dicts
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')


def getAccessToken(request):
    app = settings.objects.first()
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + app.app_id + '&secret=' + app.app_secret
    res = requests.get(url)
    print(res.text)
    return HttpResponse(res.text, content_type='application/json,charset=utf-8')


def getUserOpenid(request, js_code):
    app = settings.objects.first()
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    header = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    data = {
        'appid': app.app_id,
        'secret': app.app_secret,
        'grant_type': 'authorization_code',
        'js_code': js_code
    }
    res = requests.post(url, data, headers=header)
    print(res.text)
    return HttpResponse(res.text, content_type='application/json,charset=utf-8')


def getFilm(request, id):
    print(request, id)
    result = {'err_msg': "OK", 'objects': []}
    dicts = []
    if id == 0:
        films = film.objects.all()
        for per in films:
            video_dic = {'name': per.name,
                         'cover': per.cover, 'id': per.id}
            dicts.append(video_dic)
        result['objects'] = dicts
    else:
        films = film.objects.get(id=id)
        per = films
        dict_episodes = []
        episodes = video.objects.filter(belongTo=per)
        for per_eposide in episodes:
            dict_episodes.append({'name': per_eposide.name, 'url': per_eposide.url})
        video_dic = {'name': per.name,
                     'cover': per.cover, 'id': per.id, 'eposides': dict_episodes}
        result['objects'] = video_dic
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')
