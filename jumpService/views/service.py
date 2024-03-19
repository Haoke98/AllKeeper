# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/19
@Software: PyCharm
@disc:
======================================="""
from django.http import HttpResponse

from ..models import ServiceUser


def get_users(request):
    serviceId = request.GET.get('serviceId')
    if serviceId is None:
        return HttpResponse("参数异常/参数缺漏", status=400)
    users = ServiceUser.objects.filter(service_id=serviceId).all()
    html_str = '<table border="1">'
    html_str += "<thead><td>ID</td><td>用户名</td><td>密码</td><td>备注</td></tr></thead>"
    html_str += "<tbody>"
    for user in users:
        html_str += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (user.id, user.username,
                                                                               user.password, user.remark)
        print(html_str)
    html_str += "</table>"
    return HttpResponse(html_str)
