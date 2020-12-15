import datetime
# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .utils import analyseGetVideoInfo


# Create your views here.


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
    url = "http://localhost:7000/miniProgram/getSubcribtionAccessToken"
    access_token = requests.get(url).text
    print("this is access_token by request the local server on the server:%s" % access_token)
    return access_token


@login_required
@csrf_exempt
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
                from .utils import upLoadImg
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



def videoUrlMaker(request, vid):
    pureUrl = cache.get(vid)
    video = Video.objects.get(id=vid)
    print("thi is videoUrlMaker:", video.belongTo, video)
    video.show()
    if pureUrl is None:
        print("this video has not been saved in cache yet, getting it url now......")
        pureUrl = video.getPureVideoUrl()
        cache.set(vid, pureUrl, 8 * 60 * 60)
    else:
        print("this video has been saved in cache. has got it's pure url.")
    return redirect(to=pureUrl)


def getAllArticles(request):
    result = {'err_msg': "OK", 'objects': []}
    articles = Article.objects.order_by('-last_changed_time')
    dict_object = []
    for per in articles:
        dict_object.append(per.json())
    result['objects'] = dict_object
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')


@csrf_exempt
def getArticleInfo(request):
    data_dic = json.loads(request.body)
    url = data_dic['url']
    print(url)
    result = cache.get(url)
    if result is None:
        print("没有缓存，正在进行实时解析。。。。。。")
        res = analyseGetVideoInfo(url)
        result = json.dumps(res, ensure_ascii=False)
        cache.set(url, result, 8 * 60 * 60)
    else:
        print("已有缓存，正在返回缓存数据。。。。。。。。")
    return HttpResponse(result, content_type='application/json,charset=utf-8')


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
            text = "request:" + str(request) + "\n\n\n" + "requset.POST:" + str(
                request.POST) + "\n\n\n" + "request.GET:" + str(request.GET) + "\n\n\n" + "request.Body:" + str(
                request.body)
            send_mail('@Sadam WebSite UrlRedirection', text, '1903249375@qq.com',
                      ['1903249375@qq.com'], fail_silently=False)
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
                                    second=now.second, microsecond=now.microsecond, tzinfo=now.tzinfo)
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
        dicts.append(per.json(True))
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
    from django.utils.timezone import utc
    utcnow = datetime.datetime.utcnow().replace(tzinfo=utc)
    curr_user.last_login_time = timezone.now()
    curr_user.save()
    curr_user_json = curr_user.json()
    print(curr_user_json)
    result = {'err_msg': "OK", 'objects': [], "curr_user": curr_user_json,
              "settings": app.json()}
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')


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
