# Create your views here.
import requests
from django.http import JsonResponse

HEADERS = {
    # "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvYXBpLWV5bmVrLnF1eHJheS5jblwvYXBpXC92M1wvbXBcL2F1dGhvcml6YXRpb25zXC9mb3ItY29kZSIsImlhdCI6MTY5NTk5MzMyNCwiZXhwIjoxNjk2MDExMzI0LCJuYmYiOjE2OTU5OTMzMjQsImp0aSI6InQ3ZlJTbnZvQVJTQ3JMRjEiLCJzdWIiOjExMzQ5LCJwcnYiOiI4N2UwYWYxZWY5ZmQxNTgxMmZkZWM5NzE1M2ExNGUwYjA0NzU0NmFhIn0.l4eB_297kdgBGcGVY7hfIUR5dAPs4-F4L4n2UvWyxtc",
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvYXBpLWV5bmVrLnF1eHJheS5jblwvYXBpXC92M1wvbXBcL2F1dGhvcml6YXRpb25zXC9mb3ItY29kZSIsImlhdCI6MTY5NjA1NzYwNiwiZXhwIjoxNjk2MDc1NjA2LCJuYmYiOjE2OTYwNTc2MDYsImp0aSI6IktkZ1d6WGtVUTBHWW1HZFMiLCJzdWIiOjExMzQ5LCJwcnYiOiI4N2UwYWYxZWY5ZmQxNTgxMmZkZWM5NzE1M2ExNGUwYjA0NzU0NmFhIn0.d2JnGT2I2b0DFl4wf5VJmRseLGGkG7jEGtHMBOVSDcc",
    "authority": "api-eynek.quxray.cn",
    "xweb_xhr": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30817",
    "Referer": "https://servicewechat.com/wx0508041dfba144aa/19/page-frame.html"
}


def proxy(request, api_path: str):
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        # 允许跨域请求的源
        response['Access-Control-Allow-Origin'] = '*'
        # 允许的请求方法
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        # 允许的请求头
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    else:
        _url = f"https://api-eynek.quxray.cn/{api_path}"
        resp = requests.get(_url, headers=HEADERS, params=request.GET)
        data = {
            "path": api_path,
            "url": _url,
            "resp": resp.json()
        }
        return JsonResponse(data)
