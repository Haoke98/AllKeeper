# Create your tests here.

import requests

if __name__ == '__main__':
    url = "http://mmbiz.qpic.cn/mmbiz_png/lBSHibv6GicCap4xicp1tjTKeAddbV3JJwvjdrAGoAzqAI8icaeNdZVrK5NXWScHRosby86EgHJfibPY3OVoTCokufA/0?wx_fmt=png"
    resp = requests.get(url)
    with open("test.jpg", "wb") as f:
        f.write(resp.content)
