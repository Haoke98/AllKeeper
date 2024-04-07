# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email:1903249375@qq.com
@Date:2023/7/6
@Software: PyCharm
@disc:
======================================="""
import requests


def test(wb_id: str):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        resp = requests.get(f"https://weibo.com/u/{wb_id}", headers=headers)
        with open(f"{wb_id}.html", "wb") as f:
            f.write(resp.content)


def info(uid: str):
        """
        :return 
        {'ok': 1, 
        'data': 
                {
                    'user': {'id': 7064711748, 'idstr': '7064711748', 'pc_new': 0, 'screen_name': 'Sardarior', 'profile_image_url': 'https://tvax1.sinaimg.cn/crop.0.0.512.512.50/007I6OfGly8h896ioim87j30e80e8aae.jpg?KID=imgbed,tva&Expires=1688976518&ssig=0zay%2BiA488', 'profile_url': '/u/7064711748', 'verified': False, 'verified_type': -1, 'domain': '', 'weihao': '', 'avatar_large': 'https://tvax1.sinaimg.cn/crop.0.0.512.512.180/007I6OfGly8h896ioim87j30e80e8aae.jpg?KID=imgbed,tva&Expires=1688976518&ssig=8W5YwfQZvX', 'avatar_hd': 'https://tvax1.sinaimg.cn/crop.0.0.512.512.1024/007I6OfGly8h896ioim87j30e80e8aae.jpg?KID=imgbed,tva&Expires=1688976518&ssig=z2UP47JX%2B3', 'follow_me': False, 'following': False, 
                    'mbrank': 3, 'mbtype': 2, 'v_plus': 0, 'planet_video': False, 'description': '喜欢唱歌', 'location': '北京', 'gender': 'm', 'followers_count': 237, 'followers_count_str': '237', 'friends_count': 225, 'statuses_count': 38, 'url': '', 'svip': 0, 'cover_image_phone': 'https://ww1.sinaimg.cn/crop.0.0.640.640.640/9d44112bjw1f1xl1c10tuj20hs0hs0tw.jpg', 'icon_list': [], 'user_type': 2, 'is_star': '0', 'is_muteuser': False, 'special_follow': False},
        'tabList': [{'name': 'home', 'tabName': '精选'}, {'name': 'feed', 'tabName': '微博'}, {'name': 'newVideo', 'tabName': '视频'}, {'name': 'album', 'tabName': '相册'}], 'blockText': ''}}
        """
        resp = requests.get(f"https://weibo.com/ajax/profile/info?uid={uid}", headers={
            "Cookie": "SUB=_2AkMU0XJPf8NxqwJRmfoRxG7gboVyyw3EieKijYOUJRMxHRl-yT9kqkI9tRB6P1FcoA_jiiwlWkU1njUraklGH8yyp3eg; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5o-1D0KVWj47oMwKycwlRH; SINAGLOBAL=3835450204212.678.1670249850113; ULV=1670249850168:1:1:1:3835450204212.678.1670249850113:; XSRF-TOKEN=szpHdnejDXDZYbx6Z4qSgioL; WBPSESS=1QIptkPh0r7VTljIOfRP67LOhyoJ1yOf94TLlawIatqfNeS0xdW8Sei-I-A4Dksn0mlpb1M64xnYWdD0Pas_puBut1fMAOtq8YLZdv81Xf8Dc5AwXo-3S4K8jrf0VE5Rcj3F2sMwDYgSb4nxONnzki84VKkpLKAh5pPuJTTE-WI="
        })
        print(resp.status_code)
        contentType = resp.headers['Content-Type']
        if 'text' in contentType:
            #   print(resp.status_code,"异常:",resp.text)
              return False,None
        elif 'application/json' in contentType:
            print(resp.json())
            data = resp.json()['data']
            return True,data
        else:
              print("ContentType:",contentType)
              return False,None
        # user_info = data['user']
        # profile_image_url = user_info['profile_image_url']
        # image = urllib.request.urlopen(profile_image_url).read()
        # img = Image.open(io.BytesIO(image))
        # img.show()

    
def detail(uid: str):
        """
        :param uid: 微博里的用户系统ID
        :return:{'data': {'followers': {'total_number': 0}, 'education': {'school': '首都医科大学丰台校区'}, 'birthday': '2000-08-26 处女座', 'created_at': '2019-04-04 16:00:06', 'description': '喜欢唱歌', 'gender': 'm', 'location': '北京', 'ip_location': '', 'sunshine_credit': {'level': '信用较好'}, 'label_desc': [{'name': '视频累计播放量3.9万', 'normal_mode': {'word_color': '#FFFF6200', 'background_color': '#59FFDDCB'}, 'dark_mode': {'word_color': '#FFEA8011', 'background_color': '#FF181818'}, 'scheme_url': ''}], 'desc_text': '', 'verified_url': 'https://verified.weibo.com/verify?fr=myverified?uid=7064711748'}, 'ok': 1}
        """
        resp = requests.get(f"https://weibo.com/ajax/profile/detail?uid={uid}", headers={
            "Cookie": "SUB=_2AkMU0XJPf8NxqwJRmfoRxG7gboVyyw3EieKijYOUJRMxHRl-yT9kqkI9tRB6P1FcoA_jiiwlWkU1njUraklGH8yyp3eg; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5o-1D0KVWj47oMwKycwlRH; SINAGLOBAL=3835450204212.678.1670249850113; ULV=1670249850168:1:1:1:3835450204212.678.1670249850113:; XSRF-TOKEN=szpHdnejDXDZYbx6Z4qSgioL; WBPSESS=1QIptkPh0r7VTljIOfRP67LOhyoJ1yOf94TLlawIatqfNeS0xdW8Sei-I-A4Dksn0mlpb1M64xnYWdD0Pas_puBut1fMAOtq8YLZdv81Xf8Dc5AwXo-3S4K8jrf0VE5Rcj3F2sMwDYgSb4nxONnzki84VKkpLKAh5pPuJTTE-WI="
        })
        print(resp.json())
        return resp.json()['data']


if __name__ == '__main__':
    # detail("7064711748")
    info("7064711748")
