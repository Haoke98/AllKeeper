import datetime
# Create your views here.
import json

import requests
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from izBasar.settings import ADMINS, EMAIL_HOST_USER
from miniProgram.models import *
from miniProgram.services import SubscriptionAccountService
from miniProgram.utils import analyseGetVideoInfo, beautyDictPrint, upLoadImg

SESSION_KEY_CURR_USER_OPENID = "OPENID"
SESSION_KEY_CURR_USER = "curr_user"

subscriptionAccountService = SubscriptionAccountService()


# Create your views here.
def checkLogin(func):
    def wrapper(request, *args, **kwargs):
        # is_login = request.session.get(IS_LOGIN_KEY, False)
        # print(request, is_login)
        # if is_login:
        #     res = func(request, *args, **kwargs)
        #     res["is_login"] = True
        #     return HttpResponse(json.dumps(res, ensure_ascii=False),
        #                         content_type="application/json,charset=utf-8")  # 返回json
        # else:
        #     res = {"code": 205, "msg": "你还没有登录，请登录！", "is_login": False}
        #     return HttpResponse(json.dumps(res, ensure_ascii=False),
        #                         content_type="application/json,charset=utf-8")  # 返回json

        return func(request, *args, **kwargs)

    return wrapper


@checkLogin
def updateSystemInfo(request):
    systemInfo = request.GET.get('systemInfo')
    openid = request.session.get(SESSION_KEY_CURR_USER)
    user_json = ""
    if openid is not None:
        curr_user = User.objects.get(openid=openid)
        curr_user.systemInfo = systemInfo
        curr_user.save()
        user_json = curr_user.json()
    else:
        user_json = {"err_msg": "无效的openid"}
    text = "user:\n" + beautyDictPrint(user_json) + "\n" + str(request.GET)
    send_mail('@Sadam WebSite LoginAndUpdateSystemInfo', text, EMAIL_HOST_USER,
              [ADMINS[1][1], ], fail_silently=False)
    return HttpResponse("hello world by @Sadam!" + beautyDictPrint(user_json))


@checkLogin
@login_required
@csrf_exempt
def delete_img_from_subscriptions(request):
    media_url = request.POST.get("media_id")
    print("this is delete_img_from _subscriptions:::{ media_id:", media_url, "}")
    del_url = "https://api.weixin.qq.com/cgi-bin/material/del_material?access_token=%s" % (getAccessToken())
    res = requests.post(url=del_url, json={
        "media_id": media_url
    })
    res_json = res.json()
    print("this is the response of deletion:", res_json)
    # return HttpResponse(res_json, content_type="application/json,charset=utf-8")  # 返回json
    return HttpResponse(res)


def getAccessToken():
    """
    这个不是一个视图方法
    :return:返回的是一个公众号的AccessToken
    """
    setting = Settings.objects.get_or_create(id=1)[0]
    url = "%s/miniProgram/getSubcribtionAccessToken" % setting.host
    print(url)
    access_token = requests.get(url).text
    print("this is access_token by request the local server on the server:%s" % access_token)
    return access_token


@csrf_exempt
@login_required
def upload_temp_image(request):
    result = {}
    if request.method == 'POST':
        files = request.FILES
        if files:
            image_url_list = []
            for key in files:
                file = files.get(key)
                print(file, file.size, file.name)
                file_abs_path = os.path.abspath(file.name)
                with open(file_abs_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                access_token = getAccessToken()
                media_id, url = upLoadImg(file_abs_path, access_token, "image")
                image_url_list.append({'url': url, 'media_id': media_id, 'size': file.size})
                os.remove(file_abs_path)
                # if os.path.exists(absoulutelyFilePath):
                #     os.remove(absoulutelyFilePath)
                # self.content = None
                # image_url_list.append(handle_uploaded_file(files.get(file_name)))  # 处理上传文件

            result = {'msg': 'success', "image_list": image_url_list, }
        else:
            result = {'msg': 'failed', "image_list": []}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")  # 返回json


# 处理上传的文件
# def handle_uploaded_file(file):
#     # 分割文件名，提取拓展名
#     extension = os.path.splitext(file.name)
#     # 使用uuid4重命名文件，防止重名文件相互覆盖
#     #注意首先在项目的根目录下新建media/tempimg，或者自己使用python代码创建目录
#     file_name = '{}{}'.format(uuid.uuid4(), extension[1])
#     with open(TEMP_IMAGE_DIR + file_name, 'wb+') as destination:
#         for chunk in file.chunks():#防止文件太大导致内存溢出
#             destination.write(chunk)
#     # 返回图片的URL
#     return os.path.join(WEB_HOST_MEDIA_URL, file_name)

@cache_page(timeout=2 * 60 * 60)
def getAllHousesInfo(request):
    result = {'err_msg': "OK", 'objects': []}
    houses = House.objects.order_by('-last_changed_time')
    dict_object = []
    for per in houses:
        dict_object.append(per.json())
    result['objects'] = dict_object
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')


@checkLogin
def videoUrlMaker(request, vid):
    pureUrl = cache.get(vid)
    video = Video.objects.get(id=vid)
    video.show()
    if pureUrl is None:
        print("this video has not been saved in cache yet, getting it url now......")
        pureUrl = video.getPureVideoUrl()
        cache.set(vid, pureUrl, 8 * 60 * 60)
    else:
        print("this video has been saved in cache. has got it's pure url.")
    return redirect(to=pureUrl)


@checkLogin
def getAllArticles(request):
    result = {'err_msg': "OK", 'objects': []}
    articles = Article.objects.order_by('-last_changed_time')
    dict_object = []
    for per in articles:
        dict_object.append(per.json())
    result['objects'] = dict_object
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')


@checkLogin
def getArticleInfo(request):
    url = request.GET.get('url', None)
    result = cache.get(url)
    if result is None:
        print("there is no cache for this url , will get the cache now ..... ")
        res = analyseGetVideoInfo(url)
        result = json.dumps(res, ensure_ascii=False)
        cache.set(url, result, 8 * 60 * 60)
    else:
        print("has cache on this time, will use it .....")

    return HttpResponse(result, content_type='application/json,charset=utf-8')


@checkLogin
def updatePhoneNumber(request):
    data = json.loads(request.body)
    _openid = data['openid']
    curr_user = User.objects.get(openid=_openid)
    print(data['errMsg'])
    print(data['encryptedData'])
    print(data['iv'])
    return HttpResponse("this is updatePhoneNumber API")


@checkLogin
@csrf_exempt
def UrlRedirector(request, id):
    redirector = RedirectUrlRelation.objects.get(id=id)
    url = redirector.redirectUrl
    returnValue = redirector.returnValue
    print(request.body)
    if url == "#":
        if returnValue == "#":
            text = "request:" + str(request) + "\n\n\n" + "requset.POST:" + str(
                request.POST) + "\n\n\n" + "request.GET:" + str(request.GET) + "\n\n\n" + "request.Body:" + str(
                request.body)
            send_mail('IzBasar媒体工作室：有人登陆提醒', text, EMAIL_HOST_USER,
                      [ADMINS[1][1], ], fail_silently=False)
            return HttpResponse(request, content_type='application/json,charset=utf-8')
        else:
            return HttpResponse(returnValue)
    else:
        return redirect(to=url)


@checkLogin
@csrf_exempt
def updateUserInfo(request):
    openid = request.GET.get('openid')
    data_dic = json.loads(request.body)
    curr_user = User.objects.filter(openid=openid)[0]
    curr_user.updateUserInfo(data_dic)
    print(openid, data_dic)
    return HttpResponse("update is ok.")


@checkLogin
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
                                    second=now.second, microsecond=now.microsecond, tzinfo=now.tzinfo)
    print(newDatetime)
    curr_user.vip_expiredTime = newDatetime
    curr_user.save()
    _settings = Settings.objects.first()
    _settings.total_transaction_volume += _settings.VIPprice * 1
    _settings.save()
    text = "the user:\n" + beautyDictPrint(curr_user.json()) + "\n has bought VIP membership.\nPrice:" + str(
        _settings.VIPprice) + "RMB\nTotal transaction volume:" + str(_settings.total_transaction_volume) + " RMB"
    html = loader.render_to_string("email_templates/buy_vip.html", {"user": curr_user, "vip_price": _settings.VIPprice,
                                                                    "total_transaction_volume": _settings.total_transaction_volume})
    send_mail('IzBasar工作室：有人购买会员提醒', "有人购买会员了BuyVIP", EMAIL_HOST_USER,
              [ADMINS[0][1], ], fail_silently=False, html_message=html)
    return JsonResponse(curr_user.json())


@checkLogin
def getSlider(request):
    result = {'err_msg': "OK", 'objects': []}
    app = Settings.objects.first()
    sliders = app.sliders.order_by('-last_changed_time')
    dicts = []
    for per in sliders:
        dicts.append(per.json(True))
    result['objects'] = dicts
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')


@cache_page(2 * 60 * 60)
def getMiniProgramAccessToken(request):
    app = Settings.objects.first()
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + app.app_id + '&secret=' + app.app_secret
    res = requests.get(url)
    access_token = res.text
    print('gettingMiniProgramAccessToken:(appid:%s,appSecret:%s) %s' % (app.app_id, app.app_secret, access_token))
    return HttpResponse(access_token, content_type='application/json,charset=utf-8')


@checkLogin
@cache_page(2 * 60 * 60)
def getSubscriptionAccessToken(request):
    t = subscriptionAccountService.getAccessToken()
    return HttpResponse(t)


@checkLogin
def getUserOpenid(request, js_code):
    app = Settings.objects.first()
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
    from django.utils.timezone import utc
    utcnow = datetime.datetime.utcnow().replace(tzinfo=utc)
    curr_user.last_login_time = timezone.now()
    curr_user.save()
    request.session.setdefault(SESSION_KEY_CURR_USER_OPENID, openid)
    curr_user_json = curr_user.json()
    print(curr_user_json)
    result = {'err_msg': "OK", 'objects': [], "curr_user": curr_user_json,
              "settings": app.json()}
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')


@checkLogin
def getFilm(request, id):
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