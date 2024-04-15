# Create your views here.
import datetime
import json
import tempfile
import threading

from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from minio import Minio
from pytz import UTC

from .models import IMedia, LocalMedia
from .serializers import IMediaSerializer, LocalMediaSerializer
from .services import update, create_icloud_service, collect
from proj.secret import MINIO_STORAGE_SECRET_KEY, MINIO_STORAGE_ENDPOINT, MINIO_STORAGE_ACCESS_KEY
from proj.settings import MINIO_STORAGE_MEDIA_BUCKET_NAME, MINIO_STORAGE_USE_HTTPS, MINIO_STORAGE_CERT_CHECK

DLT = datetime.timedelta(hours=1)

VIDE_PLAYER_TYPE_MAP = {
    ".MP4": "video/mp4",
    ".MOV": "video/quicktime",
}

minio_client = Minio(
    endpoint=MINIO_STORAGE_ENDPOINT,
    access_key=MINIO_STORAGE_ACCESS_KEY,
    secret_key=MINIO_STORAGE_SECRET_KEY,
    secure=MINIO_STORAGE_USE_HTTPS,  # 根据你的MinIO服务器是否使用HTTPS来设置
    cert_check=MINIO_STORAGE_CERT_CHECK
)


def test(request):
    """
    OFFSET 结束的位置
    :param request:
    :return:
    """
    from .admin import iService
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
    from .admin import iService
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
            dlt = datetime.datetime.now() - obj.updatedAt
            if dlt < DLT:
                print(obj.thumbURL)
                return HttpResponseRedirect(obj.thumbURL)
        start = max(int(startRank) - 50, 0)
        if obj.appleId is None or obj.appleId.strip() == "":
            raise Http404("iMedia没有AppleId,无法进行查询")
        requires_2fa, _iService = create_icloud_service(obj.appleId)
        if requires_2fa:
            raise Http404("需要2FA验证")

        response = _iService.query_medias(start, limit=200)
        records: list[dict] = response['records']
        update(records, start)
        for i, record in enumerate(records):
            print(i, record["recordName"], _id, record["recordName"] == _id)
            if record["recordName"] == _id:
                _url = record["fields"]["resJPEGThumbRes"]["value"]["downloadURL"]
                print(_url)
                return HttpResponseRedirect(_url)
        raise Http404(
            f"远程更新以后也没有找到对应的媒体资源，可能这个rank值={startRank}出现了问题，[{start}~{start + 100}]")


def test2(targetObj):
    from .admin import iService
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


def preview(request):
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
    target_id = target_id.replace(" ", "+")
    context = {"filename": "", "prv_src": "", "thumb_src": ""}
    if source == "IMedia":
        targetObj = IMedia.objects.filter(id=target_id).first()
        if targetObj is None:
            return HttpResponse(f"找不到[ID:{target_id}]对应的IMedia对象")
    elif source == "LocalMedia":
        targetObj = LocalMedia.objects.filter(id=target_id).first()
        if targetObj is None:
            return HttpResponse(f"找不到[ID:{target_id}]对应的LocalMedia对象")
        context["filename"] = targetObj.filename
        try:
            prv_object_name = targetObj.prv.name
        except ValueError as e:
            if "The 'prv' attribute has no file associated with it." in str(e):
                prv_object_name = targetObj.origin.name
        download_url = minio_client.presigned_get_object(
            bucket_name=MINIO_STORAGE_MEDIA_BUCKET_NAME,
            object_name=prv_object_name,
            expires=datetime.timedelta(minutes=5)
        )
        print(f"下载预签名URL: {download_url}")
        context["prv_src"] = download_url
        pass
    else:
        return HttpResponse(f"未知source[{source}]")
    return render(request, "icloud/detail.html", context=context)


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
        return JsonResponse({
            "code": 501,
            "msg": f"参数错误[source:{source},target_id:{target_id}]"
        })
    target_id = target_id.replace(" ", "+")
    if source == "IMedia":
        targetObj = IMedia.objects.filter(id=target_id).first()
        if targetObj is None:
            return JsonResponse({
                "code": 404,
                "msg": f"找不到[ID:{target_id}]对应的IMedia对象"
            })
        else:
            print(f"targetObj:[startRank:{targetObj.startRank}, appleId:{targetObj.appleId}]")
            # TODO: 这里增加一个时间有效性判断
            collect(targetObj.startRank, targetObj.appleId)
            # FIXME: serializer = IMediaSerializer(targetObj)
            return JsonResponse({
                "code": 200,
                "msg": "ok",
                "data": {
                    "masterRecord": json.loads(targetObj.masterRecord),
                    "assetRecord": json.loads(targetObj.assetRecord)
                }
            })
    elif source == "LocalMedia":
        targetObj = LocalMedia.objects.filter(id=target_id).first()
        if targetObj is None:
            return JsonResponse({
                "code": 404,
                "msg": f"找不到[ID:{target_id}]对应的LocalMedia对象"
            })
        else:
            serializer = LocalMediaSerializer(targetObj)
            return JsonResponse({
                "code": 200,
                "msg": "ok",
                "data": serializer.data
            })
    else:
        return JsonResponse({
            "code": 501,
            "msg": f"未知source[{source}]"
        })


def sync_progress(request):
    from .services import STATUS, FINISHED_COUNT, TOTAL, STARTED_AT, EXCEPTION_MSG, EXCEPTION_TRACE_BACK
    return JsonResponse(
        data={"STATUS": STATUS, "FINISHED_COUNT": FINISHED_COUNT, "TOTAL": TOTAL, "STARTED_AT": STARTED_AT,
              "EXCEPTION_MSG": EXCEPTION_MSG, "EXCEPTION_TRACE_BACK": EXCEPTION_TRACE_BACK})


def async_upload_to_s3(temp_file, s3_key):
    # 通过 S3 存储后端将文件异步上传到 S3
    default_storage.save(s3_key, temp_file)
    temp_file.close()


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        dir_path = request.GET.get('dir_path', None)
        if dir_path:
            relative_file_path = dir_path + '/' + uploaded_file.name
        else:
            relative_file_path = uploaded_file.name

        # 保存文件到本地临时目录，可以根据实际情况修改路径
        # 创建临时文件并返回文件对象

        temp_file = tempfile.TemporaryFile(mode='w+b')
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)
        # 异步任务：将文件上传到 S3
        th = threading.Thread(target=async_upload_to_s3, args=(temp_file, relative_file_path))
        th.start()

        res = {"success": 1, "message": "上传成功!", "url": relative_file_path}
        return JsonResponse(res)
