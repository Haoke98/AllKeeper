import datetime
import json

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from .models import *


# Create your views here.
def getBanner(request):
    app = settings.objects.first()
    return redirect(to=app.banner)


def getDialogBackground(request):
    app = settings.objects.first()
    return redirect(to=app.dialogBackground)


@csrf_exempt
def updateUserInfo(request):
    openid = request.GET.get('openid')
    data_dic = json.loads(request.body)
    curr_user = User.objects.filter(openid=openid)[0]
    curr_user.updateUserInfo(data_dic)
    print(openid, data_dic)
    return HttpResponse("update is ok.")


def buyVIP(request, openid):
    curr_user = User.objects.filter(openid=openid).first()
    print(curr_user)
    now = timezone.now()
    print(now)
    new_month = now.month + 1
    new_year = now.year
    if new_month > 12:
        new_year += 1
        new_month = 1
    newDatetime = datetime.datetime(year=new_year, month=new_month, day=now.day, hour=now.hour, minute=now.minute,
                                    second=now.second, tzinfo=now.tzinfo)
    print(newDatetime)
    curr_user.vip_expiredTime = newDatetime
    curr_user.save()
    return JsonResponse(curr_user.json())


def getSlider(request):
    result = {'err_msg': "OK", 'objects': []}
    app = settings.objects.first()
    sliders = app.sliders.order_by('-last_changed_time')
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


def getSubcribtionsAccessToken(request):
    app = settings.objects.first()
    subcribtion = app.subcribtion
    print(subcribtion.app_id, subcribtion.app_secret)
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + subcribtion.app_id + "&secret=" + subcribtion.app_secret
    res = requests.get(url)
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
    res_json = res.json()
    openid = res_json['openid']
    print(res_json)
    curr_user, isCreated = User.objects.get_or_create(openid=openid,
                                                      defaults={'vip_expiredTime': timezone.now(),
                                                                })
    if (isCreated):
        print("数据库里找不到关于该用户的任何信息，创建了新的空间给该用户", curr_user)
    else:
        print("数据库里找到了了该用户", curr_user)
    curr_user.last_login_time = timezone.now()
    curr_user.save()
    curr_user_json = curr_user.json()
    print(curr_user_json)
    result = {'err_msg': "OK", 'objects': [], "curr_user": curr_user_json,
              "settings": app.json()}
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')


def getFilm(request, id):
    print(request, id)
    result = {'err_msg': "OK", 'objects': []}
    dicts = []
    if id == 0:
        films = film.objects.order_by('-last_changed_time')
        for per in films:
            video_dic = {'name': per.name,
                         'cover': per.cover, 'id': per.id}
            dicts.append(video_dic)
        result['objects'] = dicts
    else:
        films = film.objects.get(id=id)
        per = films
        dict_episodes = []
        episodes = video.objects.filter(belongTo=per).order_by('-episode_num', '-last_changed_time')
        for per_eposide in episodes:
            dict_episodes.append({'name': per_eposide.name, 'url': per_eposide.url})
        video_dic = {'name': per.name,
                     'cover': per.cover, 'id': per.id, 'eposides': dict_episodes}
        result['objects'] = video_dic
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')
