from django.contrib import admin

from izBasar.admin import BaseAdmin
from ..models import BT


@admin.register(BT)
class BtAdmin(BaseAdmin):
    list_display = ['id', 'port', 'server', 'username', 'pwd', '_url', 'basicAuthUsername',
                    'basicAuthPwd', 'updatedAt',
                    'createdAt', 'deletedAt', ]
    autocomplete_fields = []
    list_filter = ['server']
    list_display_links = ['port', 'server']
    actions = []

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "username":
            if value:
                return BaseAdmin.username(obj.username)
        if field_name == 'pwd':
            if value:
                return BaseAdmin.password(obj.pwd)
        if field_name == "basicAuthUsername":
            if value:
                return BaseAdmin.username(obj.basicAuthUsername)
        if field_name == "basicAuthPwd":
            if value:
                return BaseAdmin.password(obj.basicAuthPwd)
        if field_name == "beatsPwd":
            if value:
                return BaseAdmin.password(obj.beatsPwd)
        if field_name == "remoteMonitoringPwd":
            if value:
                return BaseAdmin.password(obj.remoteMonitoringPwd)
        return value

    def _url(self, obj):
        uri = "http://"
        if obj.basicAuthUsername and obj.basicAuthPwd:
            uri += f"{obj.basicAuthUsername}:{obj.basicAuthPwd}@"
        if obj.domain:
            uri += obj.domain
        else:
            uri += obj.server.ip
        uri += f":{obj.port}"
        if obj.path:
            uri += f"/{obj.path}"

        # return BaseAdmin.shwoUrl(uri)
        return f"""<a target="_blank" href="{uri}" >点击进入</a>"""

    _url.short_description = "入口"

    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px',
            'align': 'center'
        },
        'createdAt': {
            'width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'width': '180px',
            'align': 'left'
        },
        'port': {
            'width': '80px',
            'align': 'center'
        },
        'server': {
            'width': '340px',
            'align': 'left'
        },
        'username': {
            'width': '280px',
            'align': 'left'
        },
        'pwd': {
            'width': '200px',
            'align': 'center'
        },
        'basicAuthUsername': {
            'width': '260px',
            'align': 'left'
        },

        'basicAuthPwd': {
            'width': '200',
            'align': 'center'
        },
        'deletedAt': {
            'width': '200',
            'align': 'center'
        }
    }
