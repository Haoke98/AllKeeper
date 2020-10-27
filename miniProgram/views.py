import datetime
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .utils import getOriginalUrl


# Create your views here.

@cache_page(1 * 60 * 60)
def videoUrlMaker(request, vid):
    video = Video.objects.get(id=vid)
    articleUrl = video.url
    print(("analaysing the video url from this article:%s") % articleUrl)
    url = getOriginalUrl(articleUrl)
    return redirect(to=url)


def getAllArticles(request):
    result = {'err_msg': "OK", 'objects': []}
    articles = Article.objects.all()
    dict_object = []
    for per in articles:
        dict_object.append(per.json())
    result['objects'] = dict_object
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')


@csrf_exempt
def getArticleInfo(request):
    data_dic = json.loads(request.body)
    print(data_dic['url'])
    res = requests.get(data_dic['url']).text
    # print(res)
    title = getContent(res, 'title')
    image = getContent(res, 'image')
    description = getContent(res, 'description')
    print(title, '\n\n', image, '\n\n', description)
    result = {'err_msg': "OK", 'title': title, "description": description,
              "cover_url": image}
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')


def getContent(data, str):
    sss = '<meta property="og:%s" content="' % (str)
    head_index = data.find(sss) + sss.__len__()
    print(head_index)
    end_index = head_index + data[head_index:-1].find('" />')
    print(end_index)
    return data[head_index:end_index]


def updatePhoneNumber(request):
    data = json.loads(request.body)
    _openid = data['openid']
    curr_user = User.objects.get(openid=_openid)
    print(data['errMsg'])
    print(data['encryptedData'])
    print(data['iv'])
    return HttpResponse("this is updatePhoneNumber API")


@csrf_exempt
def UrlRedirector(request, id):
    redirector = RedirectUrlRelation.objects.get(id=id)
    url = redirector.redirectUrl
    returnValue = redirector.returnValue
    print(request.body)
    if url == "#":
        if returnValue == "#":
            return HttpResponse(request, content_type='application/json,charset=utf-8')
        else:
            return HttpResponse(returnValue)
    else:
        return redirect(to=url)


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
        dicts.append(per.json())
    result['objects'] = dicts
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')


@cache_page(2 * 60 * 60)
def getMiniProgramAccessToken(request):
    app = settings.objects.first()
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + app.app_id + '&secret=' + app.app_secret
    res = requests.get(url)
    access_token = res.text
    print('gettingMiniProgramAccessToken:(appid:%s,appSecret:%s) %s' % (app.app_id, app.app_secret, access_token))
    return HttpResponse(access_token, content_type='application/json,charset=utf-8')


@cache_page(2 * 60 * 60)
def getSubcribtionsAccessToken(request):
    app = settings.objects.first()
    subcribtion = app.subcribtion
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + subcribtion.app_id + "&secret=" + subcribtion.app_secret
    res = requests.get(url)
    access_token = res.text
    print('gettingSubcribtionAccessToken:(appid:%s,appSecret:%s) %s' % (app.app_id, app.app_secret, access_token))
    return HttpResponse(res.json()['access_token'])


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
        films = Film.objects.order_by('-last_changed_time')
        for per in films:
            dicts.append(per.json(withEpisodes=False))
        result['objects'] = dicts
    else:
        film = Film.objects.get(id=id)
        result['objects'] = film.json(withEpisodes=True)
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')
