# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/12/3
@Software: PyCharm
@disc:
======================================="""
import json
import logging
import os
import platform
import sqlite3
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from subprocess import call
from urllib.parse import urlencode

from pyicloud import PyiCloudService as __iCloudService__
from pyicloud.exceptions import PyiCloudAPIResponseException, PyiCloudFailedLoginException
from pyicloud.services.photos import PhotoAsset, PhotosService

from utils import jpeg


class IPhoto(PhotoAsset):
    # TODO: 复现isHidden, isFavorite等等出现在asset record上的属性
    pass


class IcloudService(__iCloudService__):
    COMPLETED_OF_DOWNLOAD_PHOTO = 0

    def __init__(self, apple_id,
                 password=None,
                 china_account=None,
                 cookie_directory=None,
                 verify=True,
                 client_id=None,
                 with_family=True, ):
        if china_account:
            self.HOME_ENDPOINT = "https://www.icloud.com.cn"
            self.SETUP_ENDPOINT = "https://setup.icloud.com.cn/setup/ws/1"
        super().__init__(apple_id, password, cookie_directory, verify, client_id, with_family)

    def _authenticate_with_token(self):
        """Authenticate using session token."""
        data = {
            "apple_id": self.user.get("accountName"),
            "password": self.user.get("password"),
            "accountCountryCode": self.session_data.get("account_country"),
            "dsWebAuthToken": self.session_data.get("session_token"),
            "extended_login": True,
            "trustToken": self.session_data.get("trust_token", ""),
        }

        try:
            req = self.session.post(
                "%s/accountLogin" % self.SETUP_ENDPOINT, data=json.dumps(data)
            )
            self.data = req.json()
            print("登陆结果:", self.data)
        except PyiCloudAPIResponseException as error:
            msg = "Invalid authentication token."
            print("[登陆]有可能是密码错误:", msg)
            raise PyiCloudFailedLoginException(msg, error) from error
        except Exception as e:
            print("[登陆]未知异常发生:", e)

    def handle(self, outputDir: str, recent: int, photo: PhotoAsset, modify_olds: bool, auto_delete: bool):

        def __modify_create_date__():
            if platform.system() in ["Linux", "Darwin"]:
                createdTimeStr = photo.created.strftime("%Y%m%d %H:%M:%S")
                command = f'touch {raw_path} -d "{createdTimeStr}"'
            else:
                raise Exception("请完成Windows上的文件创建时间修改方法")
            call(command, shell=True)

        def __download__():
            download = photo.download()
            with open(raw_path, 'wb') as opened_file:
                opened_file.write(download.raw.read())
            __modify_create_date__()

        logging.info(f"开始了{photo.id}, {photo.filename}, {photo.size}")
        _ext_ = str(photo.filename).split(".")[1]
        _file_name_ = f"{photo.id.replace('/', '-')}.{_ext_}"
        raw_path = os.path.join(outputDir, _file_name_)
        if os.path.exists(raw_path):
            statinfo = os.stat(raw_path)
            if photo.size > statinfo.st_size:
                logging.warning(f"文件[{raw_path}]已损坏,正在重新下载....")
                __download__()
                logging.info(f"文件[{raw_path}]重新下载成功.")
            elif photo.size < statinfo.st_size:
                # 文件名一样
                raise Exception(
                    f"出现了同名文件[{photo.filename}],\n 已有文件：[{statinfo}], \n即将下载的文件：[{photo.id, photo.created, photo.asset_date, photo.added_date, photo.filename, photo.size, photo.dimensions}]")
            else:
                if modify_olds:
                    __modify_create_date__()
        else:
            __download__()

        hasLocationInfo, lat, lng = False, None, None
        if raw_path.lower().endswith(".jpg"):
            try:
                hasLocationInfo, lat, lng = jpeg.get_gps_info(raw_path=raw_path)
            except Exception as e:
                logging.error(traceback.format_exc())

        con = sqlite3.connect(os.path.join(outputDir, 'info.db'))
        con.execute(
            'INSERT OR IGNORE INTO photos(id, created, asset_date, added_date, filename,size,dimension_x,dimension_y,lat,lng) values (?,?,?,?,?,?,?,?,?,?)',
            (photo.id, photo.created, photo.asset_date, photo.added_date, photo.filename, photo.size,
             photo.dimensions[0], photo.dimensions[1], lat, lng))
        con.commit()
        con.close()

        self.COMPLETED_OF_DOWNLOAD_PHOTO += 1
        logging.info(
            f"%0.2f%% ({self.COMPLETED_OF_DOWNLOAD_PHOTO}/{recent}):{photo.id}, {photo.filename}, {raw_path}" % (
                    self.COMPLETED_OF_DOWNLOAD_PHOTO / recent * 100))
        if auto_delete:
            photo.delete()

    def download_photo(self, outputDir: str = "./Photos", transfer_album: str = None, recent=None,
                       auto_delete: bool = False,
                       modify_olds: bool = False, max_thread_count: int = 3):
        def handle(album, recent):
            _all = album.photos
            logging.info(
                f"相册[{album.name}]里总共有{len(album)}个媒体对象（包括视频，短视频，Live实况图，动图，JPG，JPEG，PNG...etc.)")
            if recent is None:
                recent = len(album)
            if max_thread_count == 1:
                for i in range(1, recent + 1):
                    photo = next(_all)
                    self.handle(outputDir, recent, photo, modify_olds, auto_delete)
            else:
                pool = ThreadPoolExecutor(max_workers=max_thread_count)
                for i in range(1, recent + 1):
                    photo = next(_all, None)
                    pool.submit(IcloudService.handle, self, outputDir, recent, photo, modify_olds, auto_delete)
                pool.shutdown(wait=True)

        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        con = sqlite3.connect(os.path.join(outputDir, 'info.db'))
        try:
            con.execute(
                'create table photos(id varchar(255) primary key, created timestamp , asset_date timestamp , added_date timestamp ,filename varchar(255), size integer, dimension_x integer, dimension_y integer )')
        except Exception as e:
            logging.info(e)
        con.close()
        if transfer_album is None:
            handle(self.photos.all, recent)
        else:
            handle(self.photos.albums.get(transfer_album), recent)

    def query_medias(self, startRank: int = 0, endRank: int = -1, direction: str = "ASCENDING", limit: int = 10,
                     smart: str = "All Photos"):
        smartAlbum = PhotosService.SMART_FOLDERS[smart]
        recordType = smartAlbum["list_type"]
        filterBy = []
        if smartAlbum["query_filter"] is not None:
            filterBy = smartAlbum["query_filter"]
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
        url = ("%s/records/query?" % self.photos.service_endpoint) + urlencode(self.photos.params)
        print(url)
        request = self.photos.session.post(url, data=json.dumps(query), headers={"Content-type": "text/plain"})
        response = request.json()
        return response

    def media_total(self, smart: str = "All Photos"):
        objType = PhotosService.SMART_FOLDERS[smart]["obj_type"]
        url = "{}/internal/records/query/batch?{}".format(
            self.photos.service_endpoint,
            urlencode(self.photos.params),
        )
        resp = self.photos.session.post(
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
                                        "value": [objType],
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
        return responseJson, _len

    def record2iphoto(self, records):
        asset_records = {}
        master_records = []
        iPhotos = []
        for rec in records:
            if rec["recordType"] == "CPLAsset":
                master_id = rec["fields"]["masterRef"]["value"]["recordName"]
                asset_records[master_id] = rec
            elif rec["recordType"] == "CPLMaster":
                master_records.append(rec)
        master_records_len = len(master_records)
        if master_records_len:
            for master_record in master_records:
                record_name = master_record["recordName"]
                iphoto = IPhoto(self._photos, master_record, asset_records[record_name])
                iPhotos.append(iphoto)
        return iPhotos

    def delete(self, assetRecordName: str, assetRecordType: str, masterRecordChangeTag: str):
        """Deletes the photo."""
        json_data = (
            '{"query":{"recordType":"CheckIndexingState"},'
            '"zoneID":{"zoneName":"PrimarySync"}}'
        )

        json_data = (
                '{"operations":[{'
                '"operationType":"update",'
                '"record":{'
                '"recordName":"%s",'
                '"recordType":"%s",'
                '"recordChangeTag":"%s",'
                '"fields":{"isDeleted":{"value":1}'
                "}}}],"
                '"zoneID":{'
                '"zoneName":"PrimarySync"'
                '},"atomic":true}'
                % (
                    assetRecordName,
                    assetRecordType,
                    masterRecordChangeTag,
                )
        )

        endpoint = self.photos.service_endpoint
        params = urlencode(self.photos.params)
        url = f"{endpoint}/records/modify?{params}"

        return self.photos.session.post(
            url, data=json_data, headers={"Content-type": "text/plain"}
        )
