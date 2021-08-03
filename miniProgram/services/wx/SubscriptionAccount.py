class SubscriptionAccountService:
    def getAccessToken(self):
        # app = Settings.objects.get_or_create(id=1)[0]
        # subcribtion = app.subcribtion
        # url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + subcribtion.app_id + "&secret=" + subcribtion.app_secret
        # print(url)
        # res = requests.get(url)
        # res_json = res.json()
        # res_json_dic = dict(res_json)
        # errCode = res_json_dic.get("errcode", 200)
        # if errCode == 200:
        #     return HttpResponse(res.json()['access_token'])
        # else:
        #     send_mail('[IzBasar]获取公众号AccessToken失败', res.text, EMAIL_HOST_USER,
        #               [ADMINS[0][1], ], fail_silently=False)
        #     raise Http404
        #     return HttpResponse(res)
        return ""
