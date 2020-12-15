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
import time
import traceback

import requests


def analyseGetVideoInfo(url):
    res = {}
    allVid, title, image_url, description = analyseGetVid(url)
    videoList = []
    for vid in allVid:
        if "wxv_" in vid:
            print("这视频来自公众号空间：", vid)
            videoList.append(getMpVideoInfo(vid))
        else:
            # vid = vid[1:-1]
            print("这视频来自腾讯视频：", vid)
            try:
                videoList.append({"isTXV": True, "vid": vid, "url_info": [{'url': getTXVOriginalUrl(vid)}]})
            except Exception:
                traceback.print_exc()
    res = {'title': title, "cover": image_url, "description": description, "videos": videoList}
    return res


def getVideoInfo(vid):
    if "wxv_" in vid:
        print("这视频来自公众号空间：", vid)
        return getMpVideoInfo(vid)
    else:
        print("这视频来自腾讯视频：", vid)
        if "'" in vid:
            str(vid).replace("'", "")
        try:
            tx_original_url = getTXVOriginalUrl(vid)
        except:
            tx_original_url = "#"
        return {"isTXV": True, "vid": vid, "url_info": [{'url': tx_original_url}]}


def getMpVideoInfo(Vid):
    url = "https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&__biz=&mid=&idx=&vid=%s&token=&lang=zh_CN&f=json&ajax=1" % (
        Vid)
    res = requests.get(url)
    json_obj = res.json()
    url_info = json_obj['url_info']
    # print("VideoInfo:", url_info)
    return {"isTXV": False, "vid": Vid, "url_info": url_info}


def analyseGetVid(url):
    res = requests.get(url).text
    title = getContent(res, 'title')
    image = getContent(res, 'image')
    description = getContent(res, 'description')
    allVid = getVidByRe(None, "wxv_[0-9]{19}", res, None) + getVidByRe("wxv_[0-9]{19}", "vid=[A-Za-z0-9]{11}\"", res,
                                                                       ["vid=", "\""])
    return allVid, title, image, description


def getContent(data, str):
    sss = '<meta property="og:%s" content="' % (str)
    head_index = data.find(sss) + sss.__len__()
    # print(head_index)
    end_index = head_index + data[head_index:-1].find('" />')
    # print(end_index)
    return data[head_index:end_index]


def getVidByRe(avoid_pattern, patt, text, need_to_remove_inVid):
    " :param avoid_pattern 是要避免的pattern，所以先用re.sub替换其他东西来排除它的干扰。"
    if avoid_pattern is not None:
        text = re.sub(avoid_pattern, "*S*A*D*A*M*", text)
    all = re.findall(patt, text)
    res = []
    for per in all:
        if need_to_remove_inVid is not None:
            for rmo in need_to_remove_inVid:
                per = str(per).replace(rmo, "")
        if per not in res:
            res.append(per)
    return res


def analyseArticleUrl(url: str):
    r"""解析公众号文章，获取文章中的视频链接信息.

    :param url: 微信公众号文章链接.
    :returns: isTXV:视频是否来自腾讯视频
            TXVid_or_WXVid:视频ID，腾讯视频ID或者是
            , _id, format_id,original_url
    :rtype: Boolean, str,str , str     , str
    :流畅链接
        url1 = "http://mpvideo.qpic.cn/0bf22aakeaaavaaitisoqnpvbugduliabiqa.f10004.mp4?dis_k=0763c0930dfdb48ce5e80eede8b8885c\x26amp;dis_t=1603624409"
    :高清链接
        url2 = "http://mpvideo.qpic.cn/0bf22aakeaaavaaitisoqnpvbugduliabiqa.f10003.mp4?dis_k=5ddd3b16a7ee22131a714e4114a8ad75\x26amp;dis_t=1603624409"
    :超清链接
        url3 = "http://mpvideo.qpic.cn/0bf22aakeaaavaaitisoqnpvbugduliabiqa.f10002.mp4?dis_k=f91c013ec5cdc13426643ff992c4a756\x26amp;dis_t=1603624409"
    """
    isTXV = False
    Vid = ""
    _id = None
    format_id = None
    tempt_url = None
    print("正在发送HTTP请求。。。。。")
    time_start = time.time()
    print("开始时间为：", time_start)
    res = requests.get(url)
    print("已经接受请求结果，所用时间：%d , 正在进行解析。。。。。。。" % (time.time() - time_start))
    time_start = time.time()
    html = res.text
    Vid = re.search("wxv_[0-9]{19}", html)
    if Vid is None:
        Vid = re.search("'[A-Za-z0-9]{11}'", html)
        if Vid is None:
            isTXV = False
            print("this is articles is not good for analyse.")
        else:
            Vid = Vid.group()[1:-1]
            isTXV = True
    else:
        isTXV = False
        Vid = Vid.group()
        print(Vid)
        try:
            dis_k = re.search("dis_k=[A-Za-z0-9]{32}", html).group()  # 三种流畅度有三个
            dis_t = re.search("dis_t=[0-9]{10}", html).group()
            format_id = re.search("\.f[0-9]{5}\.mp4\?", html).group()[2:7]
            _id = re.search("0b[A-Za-z0-9]{33}a", html).group()
            tempt_url = "http://mpvideo.qpic.cn/%s.f%s.mp4?%s&%s&vid=%s&format_id=%s" % (
                _id, format_id, dis_k, dis_t, Vid, format_id)
            print("解析获得static信息用于加快Dynamic解析URL:%s , 所用解析时间：%d" % (tempt_url, time.time() - time_start))
        except:
            print("没有成功解析")
            dis_k = ""
            dis_t = ""
            format_id = ""
            _id = ""
            tempt_url = ""
    return isTXV, Vid, _id, format_id, tempt_url


def analyseArticleUrl2(url: str, vid: str, format_id: str, _id: str):
    r"""解析公众号文章，获取文章中的视频链接信息.

    :param vid: 视频对应的微信id(WXV_开头）
    :param format_id: 临时链接中的编码ID(决定视频流的清晰度）
    :param _id: 临时链接中的头部id
    :param url: 微信公众号文章链接.
    :return: video_original_url:视频临时链接
    :rtype:  str
    :流畅链接
        url1 = "http://mpvideo.qpic.cn/0bf22aakeaaavaaitisoqnpvbugduliabiqa.f10004.mp4?dis_k=0763c0930dfdb48ce5e80eede8b8885c\x26amp;dis_t=1603624409"
    :高清链接
        url2 = "http://mpvideo.qpic.cn/0bf22aakeaaavaaitisoqnpvbugduliabiqa.f10003.mp4?dis_k=5ddd3b16a7ee22131a714e4114a8ad75\x26amp;dis_t=1603624409"
    :超清链接
        url3 = "http://mpvideo.qpic.cn/0bf22aakeaaavaaitisoqnpvbugduliabiqa.f10002.mp4?dis_k=f91c013ec5cdc13426643ff992c4a756\x26amp;dis_t=1603624409"
    """
    res = requests.get(url)
    html = res.text
    try:
        dis_k = re.search("dis_k=[A-Za-z0-9]{32}", html).group()
        dis_t = re.search("dis_t=[0-9]{10}", html).group()
    except:
        dis_k = ""
        dis_t = ""
    # url = _id + ".f" + format_id + ".mp4?" + dis_k + "&" + dis_t + "&vid=" + vid + "&format_id=" + format_id
    temp_url = "http://mpvideo.qpic.cn/%s.f%s.mp4?%s&%s&vid=%s&format_id=%s" % (
        _id, format_id, dis_k, dis_t, vid, format_id)
    print("用已经存储过的static信息加快了解析URL:%s" % temp_url)
    return temp_url


# back_url = https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1603698121873&di=c05ae03a74ea71d30e28a663304dc8e8&imgtype=0&src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fimages%2F20180419%2Fc344e9c165944e90b664ce7beb493c2a.jpeg
# back_url = https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1602625836807&di=21e96230fe8d6aed9427a6518316e9e1&imgtype=0&src=http%3A%2F%2Fhbimg.huabanimg.com%2F04d7b2420494807ec063c077bc06c5d3908cb7b330c78-rOfl2J_fw658


#  http://mpvideo.qpic.cn/0b78imaa4aaa2iaej24sifpvaq6dbzbqadqa.f10002.mp4?dis_k=c87dc66e0ef41438b527def8417d64cc&dis_t=1604063708&vid=wxv_1574216153231638528&format_id=10002

# 2: http://mpvideo.qpic.cn/0bf22aakeaaavaaitisoqnpvbugduliabiqa.f10002.mp4?dis_k=80e910e21280af6cc751fa9f185f26e6&dis_t=1604113658&vid=wxv_1499315801156354051&format_id=10002  11：38之前访问时产生的  13:08还是有效   16:46还是有效
# 5: http://mpvideo.qpic.cn/0bf2ymafgaaavaaakp2lo5pvbq6dkpbqauya.f10002.mp4?dis_k=3ea7ba6b120a2c3601ca459ce6909053&dis_t=1604113785&vid=wxv_1496201730202664961&format_id=10002
# 6: http://mpvideo.qpic.cn/0bf2nyam4aaaqqaojc2l5vpva3wdzzxabtqa.f10002.mp4?dis_k=784f796b0cd1b710a34b5383d8d20fbc&dis_t=1604113859&vid=wxv_1496014887364460546&format_id=10002
# 7: http://mpvideo.qpic.cn/0bf2dmajyaaa54anhgckx5pvag6dtqnqbhaa.f10002.mp4?dis_k=f73b803f3e3f4a434bd4f315957059ec&dis_t=1604114379&vid=wxv_1495074457818890244&format_id=10002
# 8: http://mpvideo.qpic.cn/0bf2ri7f4ab6saah7u3vjnpw5cwdl2fd4xqa.f10002.mp4?dis_k=c4733c6b5b2483c925ff393d47357dc4&dis_t=1604114908&vid=wxv_1495972735867551746&format_id=10002
# 9: http://mpvideo.qpic.cn/0bf2smariaabhaaachskbbpvde6dcsjqcfaa.f10002.mp4?dis_k=a6ed83fb0207f3e65e116ab324acf015&dis_t=1604115065&vid=wxv_1495923623554056194&format_id=10002
# 10: http://mpvideo.qpic.cn/0b78euaaiaaa5mab32sldrpvajodaqsqabaa.f10002.mp4?dis_k=d6094e523b0df814f3053896540caff7&dis_t=1604115129&vid=wxv_1495941388461539334&format_id=10002
# 11: http://mpvideo.qpic.cn/0bf2zyd54aahuiaojbsny5pvptwd33hapxqa.f10002.mp4?dis_k=fe67f052890112df12db1579f41360cc&dis_t=1604115164&vid=wxv_1494981972392280065&format_id=10002
# 12: http://mpvideo.qpic.cn/0bf2cqamqaaawmaoa2ck5npvafgdzakabsaa.f10002.mp4?dis_k=6050002db71237b7c31f9e4689bddb2c&dis_t=1604115219&vid=wxv_1494905649917460481&format_id=10002
# 13: http://mpvideo.qpic.cn/0bf2iyoowaa4mqapav2w7vpuyrwd5ndbz2ya.f10002.mp4?dis_k=257dfb407cc3ad955665a6fc63cc400e&dis_t=1604115250&vid=wxv_1494847592562819074&format_id=10002
# 14: http://mpvideo.qpic.cn/0bf2ciaamaaaymaa63kkfvpvaewdayjaabqa.f10002.mp4?dis_k=38a9959278ab0504420e0414121f3602&dis_t=1604115716&vid=wxv_1494773214181457920&format_id=10002
# 18: http://mpvideo.qpic.cn/0bf2duaaeaaatmamqalvnfpvahodaioqaaqa.f10002.mp4?dis_k=e441d764bea92b3f99910f430a001471&dis_t=1604121100&vid=wxv_1542879888767057923&format_id=10002 13:12生成
# 19: http://mpvideo.qpic.cn/0b782iaagaaanqallntwmrpvbuwdapjaaaya.f10002.mp4?dis_k=33dcb470120faa2c9b16839525dfdfeb&dis_t=1604121197&vid=wxv_1543894429550379012&format_id=10002 13:13生成
# 20: http://mpvideo.qpic.cn/0b783maaiaaafyaonnlwjjpvbw6datnqabaa.f10002.mp4?dis_k=b8f63b22f420d8022365b3d49055fbff&dis_t=1604121236&vid=wxv_1544084339632766977&format_id=10002 13:14生成
# 21: http://mpvideo.qpic.cn/0bf23iaamaaaxuao4flwjnpvbwwda3naabqa.f10002.mp4?dis_k=fcd5987628e245c59c11e62e95014f29&dis_t=1604121269&vid=wxv_1544107727189311489&format_id=10002 13:15
# 22: http://mpvideo.qpic.cn/0b78uyaamaaagqah3et6jbpvbjwda2taabqa.f10002.mp4?dis_k=bb1c951d58c19237c37b533a0020f332&dis_t=1604121304&vid=wxv_1552436384492257281&format_id=10002 13:15
# 25: http://mpvideo.qpic.cn/0b78taaagaaa5aad7tdchbpvbggdaomaaaya.f10002.mp4?dis_k=a10d40b4590f4ecad57d3db800dbadf7&dis_t=1604121384&vid=wxv_1521378910347804673&format_id=10002 13:16
# 26: http://mpvideo.qpic.cn/0b78jeaakaaax4aphjthhvpvasodaveqabia.f10003.mp4?dis_k=dd3d4cbdbbbd3b4dac8330db156f63e7&dis_t=1604121417&vid=wxv_1527677572380164099&format_id=10003 13:17
# 27: http://mpvideo.qpic.cn/0bf2biaasaaaouaomcmhrjpfacwdbefaacia.f10002.mp4?dis_k=a70c63719328fef9028d1b26f6716179&dis_t=1604121454&vid=wxv_1281354912068222977&format_id=10002 13:17
# 28: http://mpvideo.qpic.cn/0bf2uiaaaaaajaabcnv6bbpfbiwdacraaaaa.f10004.mp4?dis_k=eeefb9e50855d34abda69a629b461ca6&dis_t=1604121480&vid=wxv_1340876362021912577&format_id=10004 13:18
# 33: http://mpvideo.qpic.cn/0bf2vmecyaairmaggoejonpvrk6dfsvqqlaa.f10002.mp4?dis_k=b7fa7f8e2894479c14d858f7b1932c19&dis_t=1604134598&vid=wxv_1555544037439438849&format_id=10002 13:19
# 34: http://mpvideo.qpic.cn/0b78euaamaaaniaf2omamfpvajodaysqabqa.f10002.mp4?dis_k=8479993c0233dc4c4da47691664c336d&dis_t=1604134947&vid=wxv_1554496853897986049&format_id=10002 17:03
# 35: http://mpvideo.qpic.cn/0bf2cmaasaaa2macbes3hvpvae6dbejqacia.f10002.mp4?dis_k=d669b2d63da6db41b6d17b13398667bc&dis_t=1604134990&vid=wxv_1513602069553872901&format_id=10002 17:03
# 36: http://mpvideo.qpic.cn/0b78ciaakaaavmahondykrpvaewdaujaabia.f10003.mp4?dis_k=cd4a3938cdd9d89c6710ef6f00419d5e&dis_t=1604135126&vid=wxv_1545801317988827137&format_id=10003 17:05
# 37: http://mpvideo.qpic.cn/0b78vqaaoaaauqahaembjrpvblgda6waabya.f10002.mp4?dis_k=61375388fdad26966c774d4147340ac8&dis_t=1604135162&vid=wxv_1555715432270118916&format_id=10002 17:06
# 38: http://mpvideo.qpic.cn/0b78guaamaaa5aaickebmfpvanoday2qabqa.f10002.mp4?dis_k=ee6cb035b2ea980e3c2db53e3cec95ac&dis_t=1604135188&vid=wxv_1555787714959114244&format_id=10002 17:06
# 39: http://mpvideo.qpic.cn/0bf2tmgdaaameiad6gejpjpvzg6dgcnqymaa.f10003.mp4?dis_k=0274d58d16c6b00fbc69dd545293561b&dis_t=1604135218&vid=wxv_1559669766565527559&format_id=10003 17:07
# 下面这两个都来自同一个公众号：subat ，而且是同一个卷集
# 41: http://mpvideo.qpic.cn/0b78jaaawaaafeakox4lizpvasgdbneaacya.f10002.mp4?dis_k=35220cd54b8526c35647c432ad920f2d&dis_t=1604135239&vid=wxv_1566939676798664707&format_id=10002 17:07
# 42: http://mpvideo.qpic.cn/0bf2teijaaaqvaaglm4e3zpubgodscmrbeaa.f10002.mp4?dis_k=86a1c666c438b0504609f654129ea10b&dis_t=1604135263&vid=wxv_1577148004644470789&format_id=10002 17:08
# 47: http://mpvideo.qpic.cn/0b78imaa4aaa2iaej24sifpvaq6dbzbqadqa.f10002.mp4?dis_k=7499c186f7b006c8822cf4df7d5d2ca2&dis_t=1604135707&vid=wxv_1574216153231638528&format_id=10002 17:15
#    http://mpvideo.qpic.cn/0b78imaa4aaa2iaej24sifpvaq6dbzbqadqa.f10002.mp4?dis_k=c87dc66e0ef41438b527def8417d64cc&dis_t=1604063708&vid=wxv_1574216153231638528&format_id=10002
#                             id 永远不变(0b开头，a结尾）         fromat_id按清晰度不一样（10002超清，10003高清，10004表情）  dis_t dynamic    vid static(wxv_开头）
#
#
#                                    static                                        dis_k 每次都不一样dynamic


def getOriginalUrl(url):
    isTXV, value = analyseArticleUrl(url)
    if (isTXV):
        return None
    else:
        print("微信公众号视频原始链接", value)
        return value


def getTXVOriginalUrl(txvid):
    print("腾讯视频ID：", txvid)
    # 构造 腾讯视频地址：
    tx_url = "https://v.qq.com/x/cover/vmp7n9h5n5535c6/%s.html" % (txvid)
    analyse_url = "https://data.zhai78.com/openTxVideo.php?url=" + tx_url
    print("this is analyse_url:", analyse_url)
    res = requests.get(analyse_url)
    print("this is res", res.text)
    res_json = res.json()
    print("this is res_json", res_json)
    jx_url = res_json['jx_url']
    print("腾讯视频的原始地址：", jx_url)
    return jx_url


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
    cmd = 'curl -F media=@"%s" "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s"' % (
        path, access_token, type)
    print("this is curlCmd:%s" % cmd)
    res = os.popen(cmd).readlines()[0]
    print(res, "\n>>>>>>>>>>>>>>>\n")
    res_json = json.loads(res)
    print(res_json)
    return res_json['media_id'], res_json['url']


try:
    pass
except:
    pass

#
if __name__ == '__main__':
    url = "https://v.douyin.com/J9pNmSD/"
    # url = " https://v.douyin.com/Jxem568/"
    url = "https://data.zhai78.com/openDyJx.php?url=%s" % url
    res = requests.get(url)
    print(res.json())
    # vid = "z0974bpqehi"
    # print(getTXVOriginalUrl(vid))
    # vid = "wxv_1566939676798664707"
    # getMpVideoInfo(vid)
    # url = "https://mp.weixin.qq.com/s/9NGra4ZlVeFwnnYtqwhxqA"
    # url = "https://mp.weixin.qq.com/s/OUy7-jMvTl1ppVPwQrE2aA"
    # url = "https://mp.weixin.qq.com/s/5Y2oOyvrmx-6fDk2U6TPHQ"
    # url = "https://mp.weixin.qq.com/s/OUy7-jMvTl1ppVPwQrE2aA"
    # res = analyseGetVideoInfo(url)
    # print(res)
    # url = "https://mp.weixin.qq.com/s?__biz=MzA4MTE2NTAxOA==&mid=100004279&idx=1&sn=0ae91db507d65690894323dd06b470ac&chksm=1f987e0228eff71499aae4d8032de56344c1d08e884f99b630d45ef44639eb244df4d611176a#rd"
#     getOriginalUrl(url)
#     url = "https://mp.weixin.qq.com/s/AOy6Mh2d9B_N8FI2TFdnAg"
#     getOriginalUrl(url)
#     # from ghost import Ghost
#     # gst = Ghost()
#     # page,resources = gst.open(url)
#     # print(page,resources)
#     # result,resources2 = gst.evaluate("document.getElementByClassName('video_fill').getAttribute('origin_src');")
#     # print(result,resources2)
# access_token = getAccessToken()
# path = r"C:\Users\19032\Pictures\cloud.jpg"
# upLoadImg(path, access_token, "image")
#     # getMedia('100004279',access_token)
