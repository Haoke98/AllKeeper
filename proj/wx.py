import random
from io import BytesIO

import requests
from PIL import Image


class WxApp:
    """
    微信基础应用模型
    """
    id: str = ""
    secret: str = ""
    _name: str = ""

    def __init__(self, id: str, secret: str, name: str = ""):
        self.id = id
        self.secret = secret
        self._name = name

    def getAccessToken(self) -> str:
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.id}&secret={self.secret}"
        resp = requests.get(url)
        if resp.status_code == 200:
            respJson = dict(resp.json())
            if respJson.__contains__("errcode"):
                raise Exception(respJson.get("errmsg"))
            accessToken = respJson['access_token']
            return accessToken
        return None


class WxApplet(WxApp):
    """
    微信小程序模型
    """
    def parseURLSchema(self, scheme: str):
        url = f"https://api.weixin.qq.com/wxa/queryscheme?access_token={self.getAccessToken()}"
        data = {
            "scheme": scheme
        }

        resp = requests.post(url, json=data)
        print(resp.json())

    def generateUrlscheme(self, query: str = "", env: str = "develop"):
        url = f"https://api.weixin.qq.com/wxa/generatescheme?access_token={self.getAccessToken()}"
        data = {
            "jump_wxa":
                {
                    "path": "pages/login/login",
                    "query": query,
                    "env_version": env
                },
            "is_expire": True,
            "expire_type": 1,
            "expire_interval": 1,
        }
        resp = requests.post(url, json=data)
        print(resp.json())
        if resp.status_code == 200:
            return resp.json()["openlink"]


class WxOfficialAccount(WxApp):
    """
    微信公众号模型
    """
    def getQrTicket(self, scene_id: str) -> str:
        url = f"https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={self.getAccessToken()}"
        data = {
            "expire_seconds": 3600,
            "action_name": "QR_SCENE",
            "action_info": {"scene": {"scene_id": scene_id}}}
        resp = requests.post(url, json=data)
        print(resp.json())
        if resp.status_code == 200:
            return resp.json()["ticket"]
        return None

    def getQr(self, scene_id: str):
        url = f"https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={self.getQrTicket(scene_id)}"
        print(url)
        resp = requests.get(url)
        tempIm = BytesIO(resp.content)
        im = Image.open(tempIm)
        im.show()


def generateRandomStr(n: int):
    l = random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a', '1', '2', '3', '4', '5', '6', '7', '8', '9'], n)
    return "".join(l)
