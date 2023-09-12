# Create your views here.
import datetime
import json
import os.path
from urllib.parse import urlencode

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from pytz import UTC

from . import iService
from .models import IMedia

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
    recordType = request.GET.get("recordType", "CPLAssetAndMasterByAddedDate")
    filterBy = []
    if startRank != -1:
        filterBy.append(
            {
                "fieldName": "startRank",
                "fieldValue": {"type": "INT64", "value": startRank},
                "comparator": "EQUALS",
            }
        )
    if endRank != -1:
        filterBy.append({
            "fieldName": "endRank",
            "fieldValue": {"type": "INT64", "value": endRank},
            "comparator": "EQUALS",
        })
    if startRank != -1 or endRank != -1:
        filterBy.append({
            "fieldName": "direction",
            "fieldValue": {"type": "STRING", "value": direction},
            "comparator": "EQUALS",
        })
    query = {
        "query": {
            "filterBy": filterBy,
            "recordType": recordType,
        },
        "resultsLimit": limit,
        "desiredKeys": [
            "resJPEGFullWidth",
            "resJPEGFullHeight",
            "resJPEGFullFileType",
            "resJPEGFullFingerprint",
            "resJPEGFullRes",
            "resJPEGLargeWidth",
            "resJPEGLargeHeight",
            "resJPEGLargeFileType",
            "resJPEGLargeFingerprint",
            "resJPEGLargeRes",
            "resJPEGMedWidth",
            "resJPEGMedHeight",
            "resJPEGMedFileType",
            "resJPEGMedFingerprint",
            "resJPEGMedRes",
            "resJPEGThumbWidth",
            "resJPEGThumbHeight",
            "resJPEGThumbFileType",
            "resJPEGThumbFingerprint",
            "resJPEGThumbRes",
            "resVidFullWidth",
            "resVidFullHeight",
            "resVidFullFileType",
            "resVidFullFingerprint",
            "resVidFullRes",
            "resVidMedWidth",
            "resVidMedHeight",
            "resVidMedFileType",
            "resVidMedFingerprint",
            "resVidMedRes",
            "resVidSmallWidth",
            "resVidSmallHeight",
            "resVidSmallFileType",
            "resVidSmallFingerprint",
            "resVidSmallRes",
            "resSidecarWidth",
            "resSidecarHeight",
            "resSidecarFileType",
            "resSidecarFingerprint",
            "resSidecarRes",
            "itemType",
            "dataClassType",
            "filenameEnc",
            "originalOrientation",
            "resOriginalWidth",
            "resOriginalHeight",
            "resOriginalFileType",
            "resOriginalFingerprint",
            "resOriginalRes",
            "resOriginalAltWidth",
            "resOriginalAltHeight",
            "resOriginalAltFileType",
            "resOriginalAltFingerprint",
            "resOriginalAltRes",
            "resOriginalVidComplWidth",
            "resOriginalVidComplHeight",
            "resOriginalVidComplFileType",
            "resOriginalVidComplFingerprint",
            "resOriginalVidComplRes",
            "isDeleted",
            "isExpunged",
            "dateExpunged",
            "remappedRef",
            "recordName",
            "recordType",
            "recordChangeTag",
            "masterRef",
            "adjustmentRenderType",
            "assetDate",
            "addedDate",
            "isFavorite",
            "isHidden",
            "orientation",
            "duration",
            "assetSubtype",
            "assetSubtypeV2",
            "assetHDRType",
            "burstFlags",
            "burstFlagsExt",
            "burstId",
            "captionEnc",
            "locationEnc",
            "locationV2Enc",
            "locationLatitude",
            "locationLongitude",
            "adjustmentType",
            "timeZoneOffset",
            "vidComplDurValue",
            "vidComplDurScale",
            "vidComplDispValue",
            "vidComplDispScale",
            "vidComplVisibilityState",
            "customRenderedValue",
            "containerId",
            "itemId",
            "position",
            "isKeyAsset",
        ],
        "zoneID": {"zoneName": "PrimarySync"},
    }
    url = ("%s/records/query?" % iService.photos.service_endpoint) + urlencode(iService.photos.params)
    print(url)
    request = iService.photos.session.post(url, data=json.dumps(query), headers={"Content-type": "text/plain"})
    response = request.json()
    return JsonResponse(response)


def count(request):
    url = "{}/internal/records/query/batch?{}".format(
        iService.photos.service_endpoint,
        urlencode(iService.photos.params),
    )
    resp = iService.photos.session.post(
        url,
        data=json.dumps(
            {
                "batch": [
                    {
                        "resultsLimit": 1,
                        "query": {
                            "filterBy": {
                                "fieldName": "indexCountID",
                                "fieldValue": {
                                    "type": "STRING_LIST",
                                    "value": ["CPLAssetByAddedDate"],
                                },
                                "comparator": "IN",
                            },
                            "recordType": "HyperionIndexCountLookup",
                        },
                        "zoneWide": True,
                        "zoneID": {"zoneName": "PrimarySync"},
                    }
                ]
            }
        ),
        headers={"Content-type": "text/plain"},
    )
    responseJson = resp.json()

    _len = responseJson["batch"][0]["records"][0]["fields"]["itemCount"][
        "value"
    ]
    print(_len)
    return JsonResponse(responseJson)


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
    target_id = request.GET.get("id")
    if target_id is None:
        return HttpResponse("请提供正确有效的ID")
    targetObj = IMedia.objects.filter(id=target_id).first()
    if targetObj is None:
        return HttpResponse(f"找不到[ID:{target_id}]对应的媒体对象")
    context = {"filename": targetObj.filename}
    if targetObj.thumb is not None and os.path.exists(targetObj.thumb.path):
        context["thumb_src"] = targetObj.thumb.url
    if targetObj.prv is not None and os.path.exists(targetObj.prv.path):
        context["prv_src"] = targetObj.prv.url
    # medias = iService.photos.all
    # target_photo = None
    # for i, photo in enumerate(medias):
    #     print(i, photo)
    #     if photo.id == target_id:
    #         target_photo = photo
    #         break
    # print("target:", target_photo)
    # download_url = iService.photos.download(target_id)
    # test()
    # test2(targetObj)
    return render(request, "icloud/detail.html", context=context)


def sync_progress(request):
    from .admin import STATUS, FINISHED_COUNT, TOTAL, STARTED_AT, EXCEPTION_MSG, EXCEPTION_TRACE_BACK
    return JsonResponse(
        data={"STATUS": STATUS, "FINISHED_COUNT": FINISHED_COUNT, "TOTAL": TOTAL, "STARTED_AT": STARTED_AT,
              "EXCEPTION_MSG": EXCEPTION_MSG, "EXCEPTION_TRACE_BACK": EXCEPTION_TRACE_BACK})
