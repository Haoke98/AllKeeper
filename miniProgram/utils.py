# import sys
#
# import bs4 as bs
# from PyQt5.QtCore import QUrl
# from PyQt5.QtWebEngineWidgets import QWebEnginePage
# from PyQt5.QtWidgets import QApplication
#
#
# class MyWebBrowser(QWebEnginePage):
#     app = None
#
#     # 类变量 QApplication
#     # 实际测试时，若调用了多个MyWebBrowser对象（有先后顺序的调用）
#     # 比如现在某些页面上，获取了所有包含图片的页面链接，再去打开这些链接上抓取图片
#     # 容易在这一步 super().__init__() 异常崩溃
#     # 可能是在 QApplication.quit()调用时，出现了资源释放异常
#     # 改成类变量控制后，没有出现崩溃现象，这个还需要再测试测试
#
#     def __init__(self):
#         if MyWebBrowser.app is None:
#             MyWebBrowser.app = QApplication(sys.argv)
#         # self.app = QApplication(sys.argv)
#         # print("DownloadDynamicPage")
#         super().__init__()
#         self.html = ''
#         # 将加载完成信号与槽连接
#         self.loadFinished.connect(self._on_load_finished)
#         # print("DownloadDynamicPage Init")
#
#     def downloadHtml(self, url):
#         """
#             将url传入，下载此url的完整HTML内容（包含js执行之后的内容）
#             貌似5.10.1自带一个download函数
#             这个在5.8.2上也是测试通过的
#         :param url:
#         :return: html
#         """
#         self.load(QUrl(url))
#         print("\nDownloadDynamicPage", url)
#         # self.app.exec_()
#         # 函数会阻塞在这，直到网络加载完成，调用了quit()方法，然后就返回html
#         # MyWebBrowser.app.exec_()
#         return self.html
#
#     def _on_load_finished(self):
#         """
#             加载完成信号的槽
#         :return:
#         """
#         self.html = self.toHtml(self.Callable)
#
#     def Callable(self, html_str):
#         """
#             回调函数
#         :param html_str:
#         :return:
#         """
#         self.html = html_str
#         MyWebBrowser.app.quit()
#         # self.app.quit()
#
#
# def useWebEngineMethod(url):
#     """
#         使用PyQt5的网页组件下载完整的动态网页
#     """
#
#     webBrowser = MyWebBrowser()
#     html = webBrowser.downloadHtml(url)
#
#     # with open("f://download_by_web_engine.html", "w+", encoding="utf-8") as f:
#     #     f.write(html)
#     return html
#
#
# def getImgUrlList(html: str):
#     """
#         从网页中解析所需要的图片的url，存储进list中
#     """
#     # 使用html.parser解析
#     soup = bs.BeautifulSoup(html, 'html.parser')
#     # 按条件查找img标签
#     pageOptionList = soup.find_all('img', class_='test')
#     print(pageOptionList)
#     imgUrlList = list()
#     for pageOptionEle in pageOptionList:
#         # 获取img标签的src中的url
#         imgUrl = pageOptionEle.get("src", None)
#         if imgUrl is None:
#             continue
#         imgUrlList.append(imgUrl)
#     return imgUrlList
#
#
import json
import os
import re

import requests


def getSubscripVideoUrl(url):
    res = requests.get(url)
    html = res.text
    base_href = 'http://mpvideo.qpic.cn/'
    start = html.find(base_href)
    print("start is this time:", start)
    if start == -1:
        txvid = re.search("'[A-Za-z0-9]{11}'", html).group()[1:-1]
        print("this is txVid:", txvid)
        return True, txvid
    else:
        vid = re.search("wxv_[0-9]{19}", html).group()
        dis_k = re.search("dis_k=[A-Za-z0-9]{32}", html).group()  # 三种流畅度有三个
        dis_t = re.search("dis_t=[0-9]{10}", html).group()
        format_id = re.search("\.f[0-9]{5}\.mp4\?", html).group()[2:7]
        _id = re.search(base_href + "[A-Za-z0-9]{36}", html).group()

        # # 流畅链接
        url1 = "http://mpvideo.qpic.cn/0bf22aakeaaavaaitisoqnpvbugduliabiqa.f10004.mp4?dis_k=0763c0930dfdb48ce5e80eede8b8885c\x26amp;dis_t=1603624409"
        # # 高清链接
        url2 = "http://mpvideo.qpic.cn/0bf22aakeaaavaaitisoqnpvbugduliabiqa.f10003.mp4?dis_k=5ddd3b16a7ee22131a714e4114a8ad75\x26amp;dis_t=1603624409"
        # # 超清链接
        url3 = "http://mpvideo.qpic.cn/0bf22aakeaaavaaitisoqnpvbugduliabiqa.f10002.mp4?dis_k=f91c013ec5cdc13426643ff992c4a756\x26amp;dis_t=1603624409"
        url = "http://mpvideo.qpic.cn/0bf22aakeaaavaaitisoqnpvbugduliabiqa.f10002.mp4?dis_k=f91c013ec5cdc13426643ff992c4a756&dis_t=1603624409&vid=wxv_1499315801156354051&format_id=10002"
        url = _id + ".f" + format_id + ".mp4?" + dis_k + "&" + dis_t + "&vid=" + vid + "&format_id=" + format_id
        return False, url


# back_url = https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1603698121873&di=c05ae03a74ea71d30e28a663304dc8e8&imgtype=0&src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fimages%2F20180419%2Fc344e9c165944e90b664ce7beb493c2a.jpeg
# back_url = https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1602625836807&di=21e96230fe8d6aed9427a6518316e9e1&imgtype=0&src=http%3A%2F%2Fhbimg.huabanimg.com%2F04d7b2420494807ec063c077bc06c5d3908cb7b330c78-rOfl2J_fw658


def getOriginalUrl(url):
    isTXV, value = getSubscripVideoUrl(url)
    if (isTXV):
        print("腾讯视频ID：", value)
        # 构造 腾讯视频地址：
        tx_url = "https://v.qq.com/x/cover/vmp7n9h5n5535c6/%s.html" % (value)
        analyse_url = "https://data.zhai78.com/openTxVideo.php?url=" + tx_url
        print("this is analyse_url:", analyse_url)
        res = requests.get(analyse_url)
        print("this is res", res.text)
        res_json = res.json()
        print("this is res_json", res_json)
        jx_url = res_json['jx_url']
        print("腾讯视频的原始地址：", jx_url)
        return jx_url
    else:
        print("微信公众号视频原始链接", value)
        return value


# if __name__ == '__main__':
#     url = "https://mp.weixin.qq.com/mp/readtemplate?t=pages/video_player_tmpl&auto=0&vid=wxv_1566939676798664707"
#     # useRequestMethod(url)
#     url = "http://mp.weixin.qq.com/s?__biz=MzA4MTE2NTAxOA==&mid=100004266&idx=1&sn=78505e41f59b33a37423e0dc973b1031&chksm=1f987e1f28eff70928be9055338de0230370a74e27de8c889ed2542f871c1f27bbb8c19df4de#rd"
#     url = "https://mp.weixin.qq.com/s/loKx7j94m4VmgyPKuxcpwQ"
#     getOriginalUrl(url)
# html = useWebEngineMethod(url)
# imgUrlList = getImgUrlList(html)
# print(imgUrlList)


# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
#
# def main(url):
#     driver = webdriver.Chrome()
#     driver.get('https://v.taobao.com/v/content/live?catetype=704&from=taonvlang')
#     soup = BeautifulSoup(driver.page_source, 'lxml')
#     for img_tag in soup.body.select('img[src]'):
#         print(img_tag.attrs['src'])
#
#
# if __name__ == '__main__':

#     main(url)
def getAccessToken(appid, appSecret):
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
        appid, appSecret)
    res = requests.get(url)
    print(res.json())
    return


def getMedia(mid, access_token):
    url = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=%s" % (access_token)
    body = {
        "media_id": mid
    }
    import json
    res = requests.post(url=url, data=json.dumps(body))
    print(res.text)


def upLoadImg(path, access_token, type):
    # https: // api.weixin.qq.com / cgi - bin / material / add_material?access_token = ACCESS_TOKEN & type = TYPE
    cmd = 'curl -F media=@%s "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s"' % (
        path, access_token, type)
    print("this is curlCmd:%s" % cmd)
    res = os.popen(cmd).readlines()[0]
    print(res, "\n>>>>>>>>>>>>>>>\n")
    res_json = json.loads(res)
    print(res_json)
    return res_json['media_id'], res_json['url']


#
if __name__ == '__main__':
    #     # url = "https://mp.weixin.qq.com/s/9NGra4ZlVeFwnnYtqwhxqA"
    #     url = "https://mp.weixin.qq.com/s?__biz=MzA4MTE2NTAxOA==&mid=100004279&idx=1&sn=0ae91db507d65690894323dd06b470ac&chksm=1f987e0228eff71499aae4d8032de56344c1d08e884f99b630d45ef44639eb244df4d611176a#rd"
    #     getOriginalUrl(url)
    #     url = "https://mp.weixin.qq.com/s/AOy6Mh2d9B_N8FI2TFdnAg"
    #     getOriginalUrl(url)
    #     # from ghost import Ghost
    #     # gst = Ghost()
    #     # page,resources = gst.open(url)
    #     # print(page,resources)
    #     # result,resources2 = gst.evaluate("document.getElementByClassName('video_fill').getAttribute('origin_src');")
    #     # print(result,resources2)
    access_token = getAccessToken()
    path = r"C:\Users\19032\Pictures\cloud.jpg"
    upLoadImg(path, access_token, "image")
#     # getMedia('100004279',access_token)
