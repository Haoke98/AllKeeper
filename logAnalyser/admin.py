import datetime
import re
import threading
from urllib.parse import urlparse

from django.contrib import admin
from simplepro.decorators import button

from utils import human_readable_bytes
from .models import NginxLog


def load_nginx_log_file():
    pattern = r'''(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (.*?) \[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\] "(\w*)\s?(.*?)\s?((HTTP)?.*?)" (\d{3}) (\d+) "(.*?)" "(.*?)"'''
    with open('/Users/shadikesadamu/Downloads/www.1.ink.log') as f:
        for i, line in enumerate(f):
            match = re.search(pattern, line)
            if match is None:
                raise Exception(f"异常记录：[{line}]")
            else:
                ip, tel, time_str, method, url, pv, status, bytes, unknown, ua = match.groups()
                time_obj = datetime.datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S %z')
                result = urlparse(url)
                print(i, time_obj, ip, method, url, pv, status, bytes, tel, unknown, ua)
                obj = NginxLog(line=i, ip=ip, tel=tel, time=time_obj, method=method, status=status,
                               path=result.path, query=result.query, pv=pv,
                               bytes=bytes,
                               unknown=unknown, userAgent=ua)
                obj.save()


# Register your models here.
@admin.register(NginxLog)
class NginxLogAdmin(admin.ModelAdmin):
    list_display = ['line', 'ip', 'time', 'method', 'status', 'bytes', 'tel', 'pv', 'unknown', 'path', 'query',
                    'userAgent']
    list_filter = ['time', 'ip', 'method', 'status', 'unknown', 'tel', 'pv', 'userAgent', 'path']
    # list_filter_multiples = ('ext', 'dimensionX', 'dimensionY',)
    search_fields = ['id', 'filename']
    actions = ['load', 'migrate']
    list_per_page = 20

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "bytes":
            if value:
                return f"""<span title="{value}">{human_readable_bytes(value)}</span>"""
        return value

    @button(type='danger', short_description='加载日志数据', enable=True, confirm="您确定要生成吗？")
    def load(self, request, queryset):
        th = threading.Thread(target=load_nginx_log_file)
        th.start()
        return {
            'state': True,
            'msg': f'开始加载日志信息'
        }

    fields_options = {
        'line': {
            'fixed': 'left',
            'width': '80px',
            'align': 'center'
        },
        'ip': {
            'width': '140px',
            'align': 'center'
        },
        'time': {
            'width': '180px',
            'align': 'center'
        },
        'method': {
            'width': '120px',
            'align': 'center'
        },

        'status': {
            'width': '100px',
            'align': 'center'
        },
        'bytes': {
            'width': '100px',
            'align': 'center'
        },
        'tel': {
            'width': '140px',
            'align': 'center'
        },
        'pv': {
            'width': '100px',
            'align': 'center'
        },
        'unknown': {
            'width': '400px',
            'align': 'center'
        },
        'path': {
            'width': '400px',
            'align': 'left'
        },
        'query': {
            'width': '400px',
            'align': 'left'
        },
        'userAgent': {
            'width': '600px',
            'align': 'center'
        },
    }
