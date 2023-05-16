# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/11/5
@Software: PyCharm
@disc:
======================================="""
# 自定义中间件
import threading
import logging
import socket

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object
local = threading.local()


class RequestLogFilter(logging.Filter):
    """
    日志过滤器，将当前请求线程的request信息保存到日志的record上下文
    record带有formater需要的信息。
    """

    def filter(self, record):
        record.hostname = getattr(local, 'hostname', None)  # 主机名称
        record.dest_ip = getattr(local, 'dest_ip', None)  # 服务器IP
        record.username = getattr(local, 'username', None)  # 用户
        record.source_ip = getattr(local, 'source_ip', None)  # 客户端IP
        return True


class RequestLogMiddleware(MiddlewareMixin):
    """
    将request的信息记录在当前的请求线程上。
    """

    def process_request(self, request):
        try:
            local.hostname = socket.gethostname()
            local.dest_ip = socket.gethostbyname(local.hostname)
            local.username = request.user
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
            if x_forwarded_for:
                source_ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
            else:
                source_ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
            local.source_ip = source_ip
        except Exception as e:
            logging.warning(f"Exception occurred during the requestLog middleware. E:[{e}]")

    def process_response(self, request, response):
        return response