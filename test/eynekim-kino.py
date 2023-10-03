# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/9/29
@Software: PyCharm
@disc:
======================================="""
import json

import requests

HEADERS = {
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvYXBpLWV5bmVrLnF1eHJheS5jblwvYXBpXC92M1wvbXBcL2F1dGhvcml6YXRpb25zXC9mb3ItY29kZSIsImlhdCI6MTY5NTk5MzMyNCwiZXhwIjoxNjk2MDExMzI0LCJuYmYiOjE2OTU5OTMzMjQsImp0aSI6InQ3ZlJTbnZvQVJTQ3JMRjEiLCJzdWIiOjExMzQ5LCJwcnYiOiI4N2UwYWYxZWY5ZmQxNTgxMmZkZWM5NzE1M2ExNGUwYjA0NzU0NmFhIn0.l4eB_297kdgBGcGVY7hfIUR5dAPs4-F4L4n2UvWyxtc",
    "authority": "api-eynek.quxray.cn",
    "xweb_xhr": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30817",
    "Referer": "https://servicewechat.com/wx0508041dfba144aa/19/page-frame.html"
}


def search(query: str):
    resp = requests.get("https://api-eynek.quxray.cn/api/v3/mp/films/search", params={
        "t": query,
        "r": "undefined",
        "c": "undefined",
        "f": "undefined",
        "page": 1
    }, headers=HEADERS)
    print(resp.url)
    print(resp.headers)
    print(json.dumps(resp.json(), indent=4, ensure_ascii=False))


def get_url(id: str):
    resp = requests.get(f"https://api-eynek.quxray.cn/api/v3/mp/films/episodes/{id}/play_url", headers=HEADERS)
    print(json.dumps(resp.json(), indent=4, ensure_ascii=False))


if __name__ == '__main__':
    # search("يەنە بىر شەھەر")
    # get_url("kZz9vWooyNW37Xj")
    # get_url("0vE6AKM921Kkjqn")
    # get_url("R40xdWArElL1vVn")
    # get_url("x5A6YK7REkaP7z3")
    # get_url("1M3kQa1Md7aNmGX")
    get_url("9bZO6WRREwWlye8")
# http://wxsnsdy.wxs.qq.com/130/20210/snssvpdownload/SH/reserved/0bc3gmaawaaammahjol6vzrfam6dbmzqacya.f10002.mp4?dis_k=046fa751dfa7eee792c05c96c8dcae00&dis_t=1695997966&play_scene=10600&auth_info=WcCgxqtMHQhu1cLE+golRkZjYh4xSA10PUcaFyVuYA1pUktuCw==&auth_key=a0bb8d11892a243a99918df6f4c4dee4",