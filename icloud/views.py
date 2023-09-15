# Create your views here.
import datetime
import json

from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from pytz import UTC

from . import iService
from .models import IMedia, LocalMedia
from .services import update

DLT = datetime.timedelta(hours=1)

VIDE_PLAYER_TYPE_MAP = {
    ".MP4": "video/mp4",
    ".MOV": "video/quicktime",
}


def test(request):
    """
    OFFSET 结束的位置
    :param request:
    :return:
    """
    limit = int(request.GET.get("limit", 10))
    startRank = int(request.GET.get("startRank", -1))
    endRank = int(request.GET.get("endRank", -1))
    direction = request.GET.get("direction", "ASCENDING")
    smart = request.GET.get("smart", "All Photos")
    response = iService.query_medias(startRank, endRank, direction, limit, smart)
    records = response['records']
    update(records, startRank)
    return JsonResponse(response)


def count(request):
    smart = request.GET.get("smart", "All Photos")
    responseJson, _ = iService.media_total(smart)
    return JsonResponse(responseJson)


def thumb(request):
    _id = request.GET.get("id", None)
    startRank = request.GET.get("startRank", None)
    if _id is None or startRank is None:
        raise Http404("参数错误")
    else:
        obj = IMedia.objects.filter(id=_id).first()
        if obj is not None:
            dlt = datetime.datetime.now(tz=UTC) - obj.updatedAt
            if dlt < DLT:
                print(obj.thumbURL)
                return HttpResponseRedirect(obj.thumbURL)
        start = max(int(startRank) - 50, 0)
        response = iService.query_medias(start, limit=200)
        records: list[dict] = response['records']
        update(records, start)
        for i, record in enumerate(records):
            print(i, record["recordName"], _id, record["recordName"] == _id)
            if record["recordName"] == _id:
                _url = record["fields"]["resJPEGThumbRes"]["value"]["downloadURL"]
                print(_url)
                return HttpResponseRedirect(_url)
        raise Http404(f"远程更新以后也没有找到对应的媒体资源，可能这个rank值={startRank}出现了问题，[{start}~{start + 100}]")


def test2(targetObj):
    version = None
    dlt = datetime.datetime.now(tz=UTC) - targetObj.updatedAt
    context = {"filename": targetObj.filename, "dlt": dlt}
    if dlt < DLT:
        # 为超过期限，没过期
        versions = json.loads(targetObj.versions)
    else:
        # 超过了期限， 需要重新获取
        if targetObj.ext in [".MP4", ".MOV"]:
            context["vide_type"] = VIDE_PLAYER_TYPE_MAP[targetObj.ext]
            smartAlbum = iService.photos.albums["Videos"]
        else:
            smartAlbum = iService.photos.albums["Live"]
        for i, p in enumerate(smartAlbum):
            obj, _ = IMedia.objects.get_or_create(id=p.id)
            obj.versions = json.dumps(p.versions, indent=4)
            obj.save()
            print(i, p)
            if p.id == targetObj.id:
                versions = p.versions

    if version is not None:
        thumb = versions["thumb"]
        print(thumb)
        context["src"] = thumb["url"]
    return context


def detail(request):
    """
    预览页面，包括视频播放和图片的展示
    :param request:
    :return:
    TODO：得实现通过临时TOKEN来进行鉴权，否则出现详情页暴露，隐私泄漏等情况
    """
    source = request.GET.get("source")
    target_id = request.GET.get("id")
    if target_id is None or source is None:
        return HttpResponse(f"参数错误[source:{source},target_id:{target_id}]")
    context = {"filename": "", "prv_src": "", "thumb_src": ""}
    if source == "IMedia":
        targetObj = IMedia.objects.filter(id=target_id).first()
        if targetObj is None:
            return HttpResponse(f"找不到[ID:{target_id}]对应的IMedia对象")
        dlt = datetime.datetime.now(tz=UTC) - targetObj.updatedAt
        if dlt > DLT:
            return HttpResponse(f"媒体对象[ID:{target_id}]的部分属性已经失去了有效性[{dlt}]")
        versions: dict = json.loads(targetObj.versions)
        # if versions.keys().__contains__("thumb"):
        prv_version = versions["thumb"]
        context["filename"] = targetObj.filename
        if prv_version["type"] in ["public.mpeg-4"]:
            context["prv_src"] = prv_version['url']
        else:
            context["thumb_src"] = prv_version['url']
    elif source == "LocalMedia":
        targetObj = LocalMedia.objects.filter(id=target_id).first()
        if targetObj is None:
            return HttpResponse(f"找不到[ID:{target_id}]对应的LocalMedia对象")
        context["filename"] = targetObj.filename
        context["prv_src"] = targetObj.prv.url
    else:
        return HttpResponse(f"未知source[{source}]")
    return render(request, "icloud/detail.html", context=context)


def sync_progress(request):
    from .services import STATUS, FINISHED_COUNT, TOTAL, STARTED_AT, EXCEPTION_MSG, EXCEPTION_TRACE_BACK
    return JsonResponse(
        data={"STATUS": STATUS, "FINISHED_COUNT": FINISHED_COUNT, "TOTAL": TOTAL, "STARTED_AT": STARTED_AT,
              "EXCEPTION_MSG": EXCEPTION_MSG, "EXCEPTION_TRACE_BACK": EXCEPTION_TRACE_BACK})
