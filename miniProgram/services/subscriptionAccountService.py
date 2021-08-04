import requests
from django.core.mail import send_mail

from izBasar.settings import EMAIL_HOST_USER, ADMINS
from miniProgram.models.subscriptionAccountModel import SubscriptionAccount


class SubscriptionAccountService:
    def getAccessToken(self):
        sas = SubscriptionAccount.objects.all()
        if len(sas) == 0:
            send_mail('[IzBasar]获取公众号AccessToken失败', "库里没有可用的订阅号", EMAIL_HOST_USER,
                      [ADMINS[0][1], ], fail_silently=False)
            raise Exception("库里没有可用的订阅号")
        else:
            sa = sas[0]
            url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + sa.appId + "&secret=" + sa.appSecret
            print(url)
            res = requests.get(url)
            resJson = res.json()
            resJsonDic = dict(resJson)
            errCode = resJsonDic.get("errcode", 200)
            if errCode == 200:
                return res.json()['access_token']
            else:
                print(resJson)
                send_mail('[IzBasar]获取公众号AccessToken失败', res.text, EMAIL_HOST_USER,
                          [ADMINS[0][1], ], fail_silently=False)
                raise Exception("获取订阅号AccessToken失败")
